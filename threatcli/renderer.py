"""Threat output rendering helpers."""

from __future__ import annotations

import json
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class _PdfLine:
    text: str
    font: str = "F1"
    size: int = 11
    color: tuple[float, float, float] = (0.0, 0.0, 0.0)
    page_break: bool = False


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


def render_pdf(threats: list[dict[str, Any]], report_meta: dict[str, Any] | None = None) -> bytes:
    """Render threats as a structured PDF report."""
    meta = _normalize_report_meta(report_meta)
    lines = _build_report_lines(threats, meta)
    pages = _paginate_lines(lines, max_lines_per_page=44)
    return _render_pdf_pages(pages)


def _normalize_report_meta(report_meta: dict[str, Any] | None) -> dict[str, Any]:
    if report_meta is None:
        report_meta = {}
    return {
        "title": str(report_meta.get("title") or "Threat Modeling Report"),
        "generated_at": str(report_meta.get("generated_at") or datetime.now(UTC).isoformat(timespec="seconds")),
        "tool_version": str(report_meta.get("tool_version") or "unknown"),
        "provider": str(report_meta.get("provider") or "unknown"),
        "model": str(report_meta.get("model") or "default"),
        "iac_inputs": [str(value) for value in report_meta.get("iac_inputs", [])],
        "doc_inputs": [str(value) for value in report_meta.get("doc_inputs", [])],
    }


def _build_report_lines(threats: list[dict[str, Any]], meta: dict[str, Any]) -> list[_PdfLine]:
    severity_counts = _count_by_severity(threats)
    discrepancy_threats = [threat for threat in threats if bool(threat.get("discrepancy_flag"))]

    lines: list[_PdfLine] = [
        _PdfLine(meta["title"], font="F2", size=18),
        _PdfLine(""),
        _PdfLine(f"Generated: {meta['generated_at']}"),
        _PdfLine(f"Tool Version: {meta['tool_version']}"),
        _PdfLine(f"Provider/Model: {meta['provider']} / {meta['model']}"),
        _PdfLine(""),
        _PdfLine("IaC Inputs", font="F2", size=12),
    ]
    if meta["iac_inputs"]:
        lines.extend(_wrapped_lines(meta["iac_inputs"], prefix="- ", font="F3"))
    else:
        lines.append(_PdfLine("- (none provided)", font="F3"))

    lines.append(_PdfLine(""))
    lines.append(_PdfLine("Design Documents", font="F2", size=12))
    if meta["doc_inputs"]:
        lines.extend(_wrapped_lines(meta["doc_inputs"], prefix="- ", font="F3"))
    else:
        lines.append(_PdfLine("- (none provided)", font="F3"))

    lines.extend(
        [
            _PdfLine(page_break=True, text=""),
            _PdfLine("Executive Summary", font="F2", size=16),
            _PdfLine(""),
            _PdfLine(f"Total Threats: {len(threats)}"),
            _PdfLine(
                f"Discrepancies Flagged: {len(discrepancy_threats)}",
                color=(0.85, 0.55, 0.0) if discrepancy_threats else (0.0, 0.0, 0.0),
            ),
            _PdfLine("Severity Breakdown", font="F2", size=12),
        ]
    )
    for severity in ("Critical", "High", "Medium", "Low", "Unspecified"):
        count = severity_counts.get(severity, 0)
        color = _severity_color(severity)
        lines.append(_PdfLine(f"- {severity}: {count}", color=color))

    lines.extend(
        [
            _PdfLine(""),
            _PdfLine("Threat Table", font="F2", size=16),
            _PdfLine(
                "ID | STRIDE | Component | Severity | Discrepancy",
                font="F3",
                size=10,
            ),
            _PdfLine("-" * 95, font="F3", size=10),
        ]
    )

    if not threats:
        lines.append(_PdfLine("No threats identified.", font="F1", size=11))
    for threat in threats:
        threat_id = str(threat.get("threat_id", "T-UNK"))
        stride = str(threat.get("stride_category", "Unknown"))
        component = str(threat.get("component", "unknown"))
        severity = _normalize_severity(str(threat.get("severity", "Unspecified")))
        discrepancy = "Yes" if bool(threat.get("discrepancy_flag")) else "No"
        row = f"{threat_id} | {stride} | {component} | [{severity}] | {discrepancy}"
        row_color = _severity_color(severity)
        if discrepancy == "Yes":
            row_color = (0.85, 0.55, 0.0)
        lines.extend(_wrapped_line(row, font="F3", size=10, color=row_color, width=94))

    lines.extend([_PdfLine(""), _PdfLine("Discrepancy Details", font="F2", size=16)])
    if not discrepancy_threats:
        lines.append(_PdfLine("No design-vs-IaC discrepancies were flagged."))
        return lines

    for threat in discrepancy_threats:
        lines.append(_PdfLine(""))
        header = (
            f"{threat.get('threat_id', 'T-UNK')} | "
            f"{threat.get('stride_category', 'Unknown')} | "
            f"{threat.get('component', 'unknown')}"
        )
        lines.append(_PdfLine(header, font="F3", size=10, color=(0.85, 0.55, 0.0)))
        detail = str(threat.get("discrepancy_detail") or threat.get("description") or "").strip()
        if not detail:
            detail = "Discrepancy flagged without detail."
        lines.extend(_wrapped_line(detail, font="F1", size=11, color=(0.2, 0.2, 0.2), width=92))

    return lines


def _wrapped_lines(items: list[str], *, prefix: str = "", font: str = "F1") -> list[_PdfLine]:
    lines: list[_PdfLine] = []
    for item in items:
        lines.extend(_wrapped_line(prefix + item, font=font, width=92))
    return lines


def _wrapped_line(
    text: str,
    *,
    font: str = "F1",
    size: int = 11,
    color: tuple[float, float, float] = (0.0, 0.0, 0.0),
    width: int = 92,
) -> list[_PdfLine]:
    wrapped = textwrap.wrap(text, width=width) or [text]
    return [_PdfLine(item, font=font, size=size, color=color) for item in wrapped]


def _count_by_severity(threats: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for threat in threats:
        counts[_normalize_severity(str(threat.get("severity", "Unspecified")))] += 1
    return counts


def _normalize_severity(severity: str) -> str:
    normalized = severity.strip().lower()
    if normalized in {"critical", "high", "medium", "low"}:
        return normalized.capitalize()
    return "Unspecified"


def _severity_color(severity: str) -> tuple[float, float, float]:
    palette = {
        "Critical": (0.65, 0.0, 0.0),
        "High": (0.75, 0.0, 0.0),
        "Medium": (0.6, 0.35, 0.0),
        "Low": (0.0, 0.45, 0.0),
        "Unspecified": (0.0, 0.0, 0.0),
    }
    return palette.get(severity, (0.0, 0.0, 0.0))


def _paginate_lines(lines: list[_PdfLine], *, max_lines_per_page: int) -> list[list[_PdfLine]]:
    pages: list[list[_PdfLine]] = []
    current: list[_PdfLine] = []
    for line in lines:
        if line.page_break:
            if current:
                pages.append(current)
            current = []
            continue
        if len(current) >= max_lines_per_page:
            pages.append(current)
            current = []
        current.append(line)
    if current:
        pages.append(current)
    return pages or [[_PdfLine("No content.")]]


def _render_pdf_pages(pages: list[list[_PdfLine]]) -> bytes:
    # 1: catalog, 2: pages root, [3..]: page/content pairs, trailing fonts.
    objects: list[bytes] = []
    page_obj_numbers: list[int] = []
    first_font_obj_number = 3 + (len(pages) * 2)
    font_numbers = {
        "F1": first_font_obj_number,
        "F2": first_font_obj_number + 1,
        "F3": first_font_obj_number + 2,
    }

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [] /Count 0 >>")

    for page_index, page_lines in enumerate(pages):
        page_obj = 3 + (page_index * 2)
        content_obj = page_obj + 1
        page_obj_numbers.append(page_obj)

        stream_data = _build_page_stream(page_lines)
        content = (
            f"<< /Length {len(stream_data)} >>\nstream\n".encode("utf-8")
            + stream_data
            + b"endstream"
        )

        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_numbers['F1']} 0 R "
                f"/F2 {font_numbers['F2']} 0 R /F3 {font_numbers['F3']} 0 R >> >> "
                f"/Contents {content_obj} 0 R >>"
            ).encode("utf-8")
        )
        objects.append(content)

    kids = " ".join(f"{obj} 0 R" for obj in page_obj_numbers)
    objects[1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_numbers)} >>".encode(
        "utf-8"
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

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


def _build_page_stream(lines: list[_PdfLine]) -> bytes:
    commands: list[bytes] = [b"BT"]
    y = 760
    for line in lines:
        safe_text = _to_pdf_text(line.text)
        escaped = _pdf_escape_text(safe_text)
        commands.append(f"/{line.font} {line.size} Tf".encode("utf-8"))
        commands.append(f"{line.color[0]:.3f} {line.color[1]:.3f} {line.color[2]:.3f} rg".encode("utf-8"))
        commands.append(f"1 0 0 1 54 {y} Tm".encode("utf-8"))
        commands.append(f"({escaped}) Tj".encode("utf-8"))
        y -= 16
    commands.append(b"ET")
    return b"\n".join(commands) + b"\n"


def _to_pdf_text(value: str) -> str:
    return value.encode("latin-1", "replace").decode("latin-1")


def _pdf_escape_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def filter_discrepancies(threats: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return only threats marked as design-vs-IaC discrepancies."""
    return [threat for threat in threats if bool(threat.get("discrepancy_flag"))]
