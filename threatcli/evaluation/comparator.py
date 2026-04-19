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

    gt_items = [_normalized_eval_item(item) for item in ground_truth]
    out_items = [_normalized_eval_item(item) for item in llm_output]
    matched_out_indices, matched_gt_indices = _match_items(out_items, gt_items)

    tp = len(matched_out_indices)
    fp = len(out_items) - tp
    fn = len(gt_items) - len(matched_gt_indices)

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
    category = _normalize_stride(str(threat.get("stride_category", "")).strip())
    return (component, category)


def _count_matched_discrepancies(
    llm_output: list[dict[str, Any]],
    ground_truth: list[dict[str, Any]],
) -> int:
    gt_discrepancies = [_normalized_eval_item(item) for item in ground_truth if bool(item.get("discrepancy_flag"))]
    out_discrepancies = [_normalized_eval_item(item) for item in llm_output if bool(item.get("discrepancy_flag"))]
    matched_out, _matched_gt = _match_items(out_discrepancies, gt_discrepancies)
    return len(matched_out)


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


def _normalize_stride(value: str) -> str:
    lowered = value.strip().lower()
    aliases = {
        "privilege escalation": "elevation of privilege",
    }
    return aliases.get(lowered, lowered)


def _normalized_eval_item(threat: dict[str, Any]) -> dict[str, str]:
    component = str(threat.get("component", "")).strip().lower()
    category = _normalize_stride(str(threat.get("stride_category", "")).strip())
    return {"component": component, "category": category}


def _component_match(output_component: str, ground_component: str) -> bool:
    if output_component == ground_component:
        return True
    if output_component == "unknown.component":
        return False
    if "." not in output_component or "." not in ground_component:
        return output_component == ground_component
    out_type, out_name = output_component.split(".", 1)
    gt_type, gt_name = ground_component.split(".", 1)
    if out_name == gt_name:
        return True
    if out_type == gt_type:
        return True
    return False


def _match_items(
    output_items: list[dict[str, str]],
    ground_items: list[dict[str, str]],
) -> tuple[set[int], set[int]]:
    matched_out: set[int] = set()
    matched_gt: set[int] = set()

    # Pass 1: exact category + exact component
    for out_idx, out_item in enumerate(output_items):
        for gt_idx, gt_item in enumerate(ground_items):
            if gt_idx in matched_gt:
                continue
            if out_item["category"] != gt_item["category"]:
                continue
            if out_item["component"] == gt_item["component"]:
                matched_out.add(out_idx)
                matched_gt.add(gt_idx)
                break

    # Pass 2: exact category + fuzzy component
    for out_idx, out_item in enumerate(output_items):
        if out_idx in matched_out:
            continue
        for gt_idx, gt_item in enumerate(ground_items):
            if gt_idx in matched_gt:
                continue
            if out_item["category"] != gt_item["category"]:
                continue
            if _component_match(out_item["component"], gt_item["component"]):
                matched_out.add(out_idx)
                matched_gt.add(gt_idx)
                break

    return matched_out, matched_gt
