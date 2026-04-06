"""Design document parsing and chunking utilities."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_MAX_CHUNK_TOKENS = int(os.getenv("TM_MAX_CHUNK_TOKENS", "1500"))
DEFAULT_OVERLAP_TOKENS = int(os.getenv("TM_OVERLAP_TOKENS", "100"))
DEFAULT_MAX_DOC_TOKENS = int(os.getenv("TM_MAX_DOC_TOKENS", "15000"))


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    heading: str
    heading_level: int
    text: str
    section_index: int
    token_estimate: int
    has_overlap: bool


def parse_document(
    path: str | Path,
    *,
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
    max_doc_tokens: int = DEFAULT_MAX_DOC_TOKENS,
) -> list[DocumentChunk]:
    """Parse markdown/txt document into heading-aware chunks."""
    doc_path = Path(path)
    if not doc_path.exists():
        raise ValueError(f"Design document path does not exist: {doc_path}")
    if doc_path.suffix.lower() not in {".md", ".txt"}:
        raise ValueError(f"Unsupported document extension '{doc_path.suffix}'. Use .md or .txt")

    text = doc_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []

    sections = _extract_sections(text)
    chunks: list[DocumentChunk] = []
    chunk_index = 1
    total_tokens = 0

    for section_index, (heading, level, body) in enumerate(sections):
        if not body.strip():
            continue

        section_chunks = _split_section(body, max_chunk_tokens=max_chunk_tokens, overlap_tokens=overlap_tokens)
        for i, chunk_text in enumerate(section_chunks):
            tokens = _estimate_tokens(chunk_text)
            if total_tokens + tokens > max_doc_tokens:
                return chunks
            total_tokens += tokens

            chunks.append(
                DocumentChunk(
                    chunk_id=f"chunk_{chunk_index:03d}",
                    heading=heading,
                    heading_level=level,
                    text=chunk_text,
                    section_index=section_index,
                    token_estimate=tokens,
                    has_overlap=i > 0,
                )
            )
            chunk_index += 1

    return chunks


def parse_documents(
    paths: Iterable[str | Path],
    *,
    max_chunk_tokens: int = DEFAULT_MAX_CHUNK_TOKENS,
    overlap_tokens: int = DEFAULT_OVERLAP_TOKENS,
    max_doc_tokens: int = DEFAULT_MAX_DOC_TOKENS,
) -> list[DocumentChunk]:
    """Parse one or more document paths (files or directories) into ordered chunks."""
    files = discover_doc_files(paths)
    chunks: list[DocumentChunk] = []
    chunk_index = 1
    total_tokens = 0

    for file_path in files:
        doc_chunks = parse_document(
            file_path,
            max_chunk_tokens=max_chunk_tokens,
            overlap_tokens=overlap_tokens,
            max_doc_tokens=max_doc_tokens,
        )
        for chunk in doc_chunks:
            if total_tokens + chunk.token_estimate > max_doc_tokens:
                return chunks
            total_tokens += chunk.token_estimate
            chunks.append(
                DocumentChunk(
                    chunk_id=f"chunk_{chunk_index:03d}",
                    heading=chunk.heading,
                    heading_level=chunk.heading_level,
                    text=chunk.text,
                    section_index=len(chunks),
                    token_estimate=chunk.token_estimate,
                    has_overlap=chunk.has_overlap,
                )
            )
            chunk_index += 1

    return chunks


def discover_doc_files(paths: Iterable[str | Path]) -> list[Path]:
    """Resolve files/directories to concrete .md/.txt paths."""
    discovered: list[Path] = []
    seen: set[Path] = set()

    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            raise ValueError(f"Design document path does not exist: {path}")

        if path.is_dir():
            candidates = sorted([*path.glob("**/*.md"), *path.glob("**/*.txt")])
        else:
            suffix = path.suffix.lower()
            candidates = [path] if suffix in {".md", ".txt"} else []

        for candidate in candidates:
            absolute = candidate.resolve()
            if absolute not in seen:
                discovered.append(candidate)
                seen.add(absolute)

    return discovered


def _extract_sections(text: str) -> list[tuple[str, int, str]]:
    lines = text.splitlines()
    sections: list[tuple[str, int, list[str]]] = []
    current_heading = "Document"
    current_level = 0
    buffer: list[str] = []

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    for line in lines:
        match = heading_pattern.match(line)
        if match:
            if buffer:
                sections.append((current_heading, current_level, buffer))
                buffer = []
            current_heading = match.group(2).strip()
            current_level = len(match.group(1))
            continue
        buffer.append(line)

    if buffer:
        sections.append((current_heading, current_level, buffer))

    return [(heading, level, "\n".join(body).strip()) for heading, level, body in sections]


def _split_section(text: str, *, max_chunk_tokens: int, overlap_tokens: int) -> list[str]:
    max_chars = max(1, max_chunk_tokens * 4)
    overlap_chars = max(0, overlap_tokens * 4)
    normalized = text.strip()
    if len(normalized) <= max_chars:
        return [normalized]

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", normalized) if p.strip()]
    if not paragraphs:
        return [normalized[:max_chars]]

    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            tail = current[-overlap_chars:] if overlap_chars else ""
            current = f"{tail}\n\n{paragraph}".strip() if tail else paragraph
        else:
            start = 0
            while start < len(paragraph):
                end = min(start + max_chars, len(paragraph))
                piece = paragraph[start:end]
                if chunks and overlap_chars:
                    piece = f"{chunks[-1][-overlap_chars:]}\n\n{piece}".strip()
                chunks.append(piece)
                if end == len(paragraph):
                    current = ""
                    break
                start = max(0, end - overlap_chars)

    if current:
        chunks.append(current)

    return chunks


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)
