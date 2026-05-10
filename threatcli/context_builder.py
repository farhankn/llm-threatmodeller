"""Prompt context assembly logic for IaC-only mode."""

from __future__ import annotations

import copy
import math
import re
import warnings
from pathlib import Path
from typing import Any

from threatcli.parsers.doc_parser import DocumentChunk
from threatcli.parsers.iac_parser import serialize_resource_map

DEFAULT_TOKEN_BUDGET = 3000
DEFAULT_IAC_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system_iac_only.txt"
DEFAULT_MULTISOURCE_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system_multisource.txt"


class TokenBudgetExceededWarning(UserWarning):
    """Raised when prompt context must be truncated to fit budget."""


def build_iac_prompt(
    resource_map: dict[str, Any],
    *,
    token_budget: int = DEFAULT_TOKEN_BUDGET,
    system_prompt_path: Path = DEFAULT_IAC_PROMPT_PATH,
) -> dict[str, str]:
    """Build the system/user message pair for IaC-only threat analysis."""
    system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()
    summary = serialize_resource_map(resource_map)

    working_map = copy.deepcopy(resource_map)
    truncation_steps: list[str] = []

    while _estimate_tokens(summary) > token_budget:
        changed = False

        if working_map.get("modules"):
            working_map["modules"] = []
            truncation_steps.append("modules")
            changed = True
        elif working_map.get("variables"):
            working_map["variables"] = []
            truncation_steps.append("variables")
            changed = True
        elif working_map.get("data_sources"):
            working_map["data_sources"] = []
            truncation_steps.append("data_sources")
            changed = True
        else:
            for resource in working_map.get("resources", []):
                if isinstance(resource, dict) and resource.get("attributes"):
                    resource["attributes"] = {}
                    changed = True
            if changed:
                truncation_steps.append("resource_attributes")

        if not changed:
            break

        summary = serialize_resource_map(working_map)

    if truncation_steps:
        warnings.warn(
            TokenBudgetExceededWarning(
                "Token budget exceeded; truncated sections in order: " + ", ".join(truncation_steps)
            ),
            stacklevel=2,
        )

    user_prompt = (
        "### Infrastructure Summary\n"
        f"{summary}\n\n"
        "### Task\n"
        "Identify realistic STRIDE threats grounded in the infrastructure summary. "
        "Return JSON only."
    )

    return {"system": system_prompt, "user": user_prompt}


def _estimate_tokens(text: str) -> int:
    """Approximate token count from character length."""
    return math.ceil(len(text) / 4)


def build_multisource_prompt(
    resource_map: dict[str, Any],
    document_chunks: list[DocumentChunk],
    *,
    token_budget: int = DEFAULT_TOKEN_BUDGET,
    system_prompt_path: Path = DEFAULT_MULTISOURCE_PROMPT_PATH,
) -> dict[str, str]:
    """Build a prompt from IaC summary plus selected document chunks."""
    system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()
    summary = serialize_resource_map(resource_map)
    summary_tokens = _estimate_tokens(summary)
    remaining_budget = max(0, token_budget - summary_tokens)

    selected_chunks = _select_chunks(
        document_chunks,
        token_budget=remaining_budget,
        resource_map=resource_map,
    )
    chunk_block = "\n\n".join(
        (
            f"[{chunk.chunk_id}] Heading: {chunk.heading} (H{chunk.heading_level})\n"
            f"{chunk.text}"
        )
        for chunk in selected_chunks
    )

    user_prompt = (
        "### Infrastructure Summary\n"
        f"{summary}\n\n"
        "### Design Document Context\n"
        f"{chunk_block if chunk_block else '(No relevant design context provided)'}\n\n"
        "### Task\n"
        "Identify realistic STRIDE threats grounded in the infrastructure summary and design context. "
        "Flag discrepancies where design intent conflicts with IaC reality. Return JSON only."
    )
    return {"system": system_prompt, "user": user_prompt}


def _extract_resource_keywords(resource_map: dict[str, Any]) -> set[str]:
    keywords = set()
    for res in resource_map.get("resources", []):
        if not isinstance(res, dict):
            continue

        r_name = str(res.get("name", "")).strip()
        r_type = str(res.get("type", "")).strip()

        for candidate in _keyword_candidates(r_name):
            keywords.add(candidate)
        for candidate in _keyword_candidates(r_type):
            keywords.add(candidate)
        if r_type and r_name:
            for candidate in _keyword_candidates(f"{r_type}.{r_name}"):
                keywords.add(candidate)

        attributes = res.get("attributes")
        if isinstance(attributes, dict):
            tags = attributes.get("tags")
            if isinstance(tags, dict):
                for tag_key in ("acse_component", "component", "name", "Name"):
                    value = tags.get(tag_key)
                    if isinstance(value, str):
                        for candidate in _keyword_candidates(value):
                            keywords.add(candidate)
    return keywords


def _score_chunk(chunk: DocumentChunk, resource_keywords: set[str], total_chunks: int) -> float:
    text_lower = chunk.text.lower()
    heading_lower = chunk.heading.lower()
    normalized_text = _normalize_keyword(f"{chunk.heading} {chunk.text}")
    
    # 1. Keyword overlap (0.40): presence of Terraform resource names
    overlap_count = 0
    for keyword in resource_keywords:
        normalized_keyword = _normalize_keyword(keyword)
        if not normalized_keyword:
            continue
        if keyword in text_lower or normalized_keyword in normalized_text:
            overlap_count += 1
    overlap_score = min(1.0, overlap_count / 5.0)  # cap at 5 matches
    
    # 2. Security keyword density (0.30)
    security_terms = {
        "security",
        "encrypt",
        "auth",
        "iam",
        "policy",
        "vpc",
        "tls",
        "ssl",
        "secret",
        "password",
        "key",
        "stride",
        "threat",
        "risk",
        "access",
        "public",
        "private",
        "firewall",
        "sg",
        "waf",
        "spoofing",
        "tampering",
        "repudiation",
        "disclosure",
        "denial",
        "privilege",
    }
    sec_count = sum(1 for term in security_terms if term in text_lower)
    sec_score = min(1.0, sec_count / 5.0)
    
    # 3. Heading relevance (0.20)
    heading_sec_terms = {"security", "architecture", "design", "infrastructure", "network", "auth", "threat"}
    heading_score = 1.0 if any(term in heading_lower for term in heading_sec_terms) else 0.0
    
    # 4. Position bonus (0.10)
    position_score = max(0.0, 1.0 - (chunk.section_index / max(1, total_chunks)))
    
    return (0.40 * overlap_score) + (0.30 * sec_score) + (0.20 * heading_score) + (0.10 * position_score)


def _select_chunks(chunks: list[DocumentChunk], *, token_budget: int, resource_map: dict[str, Any] = None) -> list[DocumentChunk]:
    if not chunks:
        return []
        
    resource_keywords = _extract_resource_keywords(resource_map) if resource_map else set()
    total_chunks = len(chunks)
    
    scored_chunks = [
        (chunk, _score_chunk(chunk, resource_keywords, total_chunks))
        for chunk in chunks
    ]
    
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    selected: list[DocumentChunk] = []
    consumed = 0
    for chunk, _ in scored_chunks:
        if consumed + chunk.token_estimate > token_budget:
            continue # Skip and try to fit smaller chunks if any
        selected.append(chunk)
        consumed += chunk.token_estimate

    # If nothing fits inside a very small budget, keep the top-ranked chunk.
    if not selected and scored_chunks:
        selected = [scored_chunks[0][0]]
        
    selected.sort(key=lambda item: (item.section_index, item.chunk_id))
    return selected


def _normalize_keyword(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.strip().lower())


def _keyword_candidates(value: str) -> set[str]:
    text = value.strip().lower()
    if not text:
        return set()
    normalized = _normalize_keyword(text)
    candidates = {text}
    if normalized:
        candidates.add(normalized)
    return candidates
