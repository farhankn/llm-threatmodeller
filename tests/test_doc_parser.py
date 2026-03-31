from pathlib import Path

import pytest

from threatcli.parsers.doc_parser import parse_document


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
