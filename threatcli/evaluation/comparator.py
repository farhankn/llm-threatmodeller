"""Ground truth / output comparison helpers for scenario-level evaluation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from threatcli.evaluation.metrics import ddr, hallucination_rate, precision, recall


def load_ground_truth(fixture_path: str | Path) -> list[dict[str, Any]]:
    path = Path(fixture_path)
    if path.is_dir():
        path = path / "ground_truth.json"
    if not path.exists():
        raise FileNotFoundError(f"Ground truth file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("ground_truth.json must contain a JSON array")
    return data


def load_llm_output(output_json: str | Path) -> list[dict[str, Any]]:
    path = Path(output_json)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = json.loads(str(output_json))
    if not isinstance(data, list):
        raise ValueError("LLM output must be a JSON array")
    return data


def build_known_components(resource_map: dict[str, Any]) -> set[str]:
    components: set[str] = set()
    for resource in resource_map.get("resources", []):
        if not isinstance(resource, dict):
            continue
        r_type = str(resource.get("type", "")).strip()
        r_name = str(resource.get("name", "")).strip()
        if r_type:
            components.add(r_type)
        if r_name:
            components.add(r_name)
        if r_type and r_name:
            components.add(f"{r_type}.{r_name}")
    return components


def compare(
    llm_output: list[dict[str, Any]],
    ground_truth: list[dict[str, Any]],
    resource_map: dict[str, Any],
) -> dict[str, Any]:
    known_components = build_known_components(resource_map)

    gt_signatures = {_threat_signature(item) for item in ground_truth}
    output_signatures = {_threat_signature(item) for item in llm_output}

    tp = len(output_signatures & gt_signatures)
    fp = len(output_signatures - gt_signatures)
    fn = len(gt_signatures - output_signatures)

    matched_discrepancies = _count_matched_discrepancies(llm_output, ground_truth)
    planted_discrepancies = sum(1 for item in ground_truth if bool(item.get("discrepancy_flag")))

    hallucinated_count = sum(1 for item in llm_output if _is_hallucinated(item, known_components))

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision(tp, fp),
        "recall": recall(tp, fn),
        "ddr": ddr(matched_discrepancies, planted_discrepancies),
        "hallucination_rate": hallucination_rate(hallucinated_count, len(llm_output)),
        "matched_discrepancies": matched_discrepancies,
        "planted_discrepancies": planted_discrepancies,
    }


def _threat_signature(threat: dict[str, Any]) -> tuple[str, str]:
    component = str(threat.get("component", "")).strip().lower()
    category = str(threat.get("stride_category", "")).strip().lower()
    return (component, category)


def _count_matched_discrepancies(
    llm_output: list[dict[str, Any]],
    ground_truth: list[dict[str, Any]],
) -> int:
    gt_discrepancy_signatures = {
        _threat_signature(item) for item in ground_truth if bool(item.get("discrepancy_flag"))
    }
    output_discrepancy_signatures = {
        _threat_signature(item) for item in llm_output if bool(item.get("discrepancy_flag"))
    }
    return len(gt_discrepancy_signatures & output_discrepancy_signatures)


def _is_hallucinated(threat: dict[str, Any], known_components: set[str]) -> bool:
    component = str(threat.get("component", "")).strip()
    if not component:
        return True
    if component in known_components:
        return False
    if "." in component:
        resource_type, resource_name = component.split(".", 1)
        if resource_type in known_components or resource_name in known_components:
            return False
    return True
