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


def filter_discrepancies(threats: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return only threats marked as design-vs-IaC discrepancies."""
    return [threat for threat in threats if bool(threat.get("discrepancy_flag"))]
