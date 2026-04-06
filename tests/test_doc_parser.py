from pathlib import Path

import pytest

from threatcli.parsers.doc_parser import discover_doc_files, parse_document, parse_documents


def test_parse_markdown_document_chunks_with_headings(tmp_path: Path) -> None:
    doc = tmp_path / "design.md"
    doc.write_text(
        (
            "# Architecture\n"
            "System uses API gateway and lambda.\n\n"
            "## Security\n"
            "Authentication via JWT.\n"
        ),
        encoding="utf-8",
    )

    chunks = parse_document(doc)

    assert chunks
    assert chunks[0].heading == "Architecture"
    assert chunks[0].heading_level == 1
    assert "API gateway" in chunks[0].text


def test_parse_document_rejects_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"
    with pytest.raises(ValueError):
        parse_document(missing)


def test_parse_document_returns_empty_for_blank_file(tmp_path: Path) -> None:
    doc = tmp_path / "empty.md"
    doc.write_text("\n", encoding="utf-8")
    assert parse_document(doc) == []


def test_discover_doc_files_supports_directory(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("# A\ntext", encoding="utf-8")
    (docs / "b.txt").write_text("notes", encoding="utf-8")
    (docs / "skip.tf").write_text("resource {}", encoding="utf-8")

    files = discover_doc_files([docs])
    names = sorted(path.name for path in files)
    assert names == ["a.md", "b.txt"]


def test_parse_documents_combines_multiple_files(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.txt"
    a.write_text("# Architecture\napi", encoding="utf-8")
    b.write_text("Security baseline text", encoding="utf-8")

    chunks = parse_documents([a, b])
    assert len(chunks) >= 2
    assert chunks[0].chunk_id == "chunk_001"
