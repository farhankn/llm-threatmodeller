"""Threat output rendering helpers."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any


def render_text(threats: list[dict[str, Any]]) -> str:
    """Render threats grouped by STRIDE category for terminal output."""
    if not threats:
        return "No threats identified."

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for threat in threats:
        category = str(threat.get("stride_category", "Unknown"))
        grouped[category].append(threat)

    lines: list[str] = []
    for category in sorted(grouped):
        lines.append(f"[{category}]")
        for threat in grouped[category]:
            threat_id = threat.get("threat_id", "T-UNK")
            severity = threat.get("severity", "Unspecified")
            component = threat.get("component", "unknown")
            description = threat.get("description", "")
            lines.append(f"- {threat_id} ({severity}) {component}: {description}")

    return "\n".join(lines)


def render_json(threats: list[dict[str, Any]]) -> str:
    """Render threats as a JSON string."""
    return json.dumps(threats, indent=2)


def render_pdf(threats: list[dict[str, Any]]) -> bytes:
    """Render threats as a simple PDF document."""
    text = render_text(threats)
    lines = text.splitlines() or [text]
    max_lines_per_page = 48
    pages = [
        lines[start : start + max_lines_per_page]
        for start in range(0, len(lines), max_lines_per_page)
    ] or [[]]

    # Keep object graph simple and deterministic:
    # 1: catalog, 2: pages root, [3..]: page/content pairs, last: font.
    objects: list[bytes] = []
    page_obj_numbers: list[int] = []
    font_obj_number = 3 + (len(pages) * 2)

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [] /Count 0 >>")

    for page_index, page_lines in enumerate(pages):
        page_obj = 3 + (page_index * 2)
        content_obj = page_obj + 1
        page_obj_numbers.append(page_obj)

        text_lines = [b"BT", b"/F1 11 Tf", b"14 TL", b"54 760 Td"]
        for line in page_lines:
            escaped = _pdf_escape_text(line)
            text_lines.append(f"({escaped}) Tj".encode("utf-8"))
            text_lines.append(b"T*")
        text_lines.append(b"ET")
        stream_data = b"\n".join(text_lines) + b"\n"
        content = (
            f"<< /Length {len(stream_data)} >>\nstream\n".encode("utf-8")
            + stream_data
            + b"endstream"
        )
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_obj_number} 0 R >> >> "
                f"/Contents {content_obj} 0 R >>"
            ).encode("utf-8")
        )
        objects.append(content)

    kids = " ".join(f"{obj} 0 R" for obj in page_obj_numbers)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_numbers)} >>".encode(
        "utf-8"
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("utf-8"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("utf-8"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("utf-8"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("utf-8")
    )
    return bytes(pdf)


def _pdf_escape_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def filter_discrepancies(threats: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return only threats marked as design-vs-IaC discrepancies."""
    return [threat for threat in threats if bool(threat.get("discrepancy_flag"))]
