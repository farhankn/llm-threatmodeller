"""Ground truth / output comparison helpers for scenario-level evaluation."""

from __future__ import annotations

import json
import re
from collections import Counter
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
    stride_tp, stride_total, stride_tfc_recall = _stride_framework_coverage(llm_output, ground_truth)
    mitre_tp, mitre_total, mitre_tfc_recall = _mitre_framework_coverage(llm_output, ground_truth)

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
        "stride_tfc_tp": stride_tp,
        "stride_tfc_total": stride_total,
        "stride_tfc_recall": stride_tfc_recall,
        "mitre_tfc_tp": mitre_tp,
        "mitre_tfc_total": mitre_total,
        "mitre_tfc_recall": mitre_tfc_recall,
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
        
    out_parts = output_component.split(".", 1)
    gt_parts = ground_component.split(".", 1)

    out_name = out_parts[-1]
    gt_name = gt_parts[-1]
    
    if out_name == gt_name:
        return True
        
    out_type = out_parts[0] if len(out_parts) == 2 else None
    gt_type = gt_parts[0] if len(gt_parts) == 2 else None
    
    if out_type and gt_type and out_type == gt_type:
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


def _stride_framework_coverage(
    llm_output: list[dict[str, Any]],
    ground_truth: list[dict[str, Any]],
) -> tuple[int, int, float]:
    gt_labels = _collect_stride_labels(ground_truth)
    out_labels = _collect_stride_labels(llm_output)
    tp, total = _coverage_recall_counts(gt_labels, out_labels)
    recall_value = tp / total if total else 0.0
    return tp, total, recall_value


def _mitre_framework_coverage(
    llm_output: list[dict[str, Any]],
    ground_truth: list[dict[str, Any]],
) -> tuple[int, int, float]:
    gt_labels = _collect_mitre_ids(ground_truth)
    out_labels = _collect_mitre_ids(llm_output)
    tp, total = _coverage_recall_counts(gt_labels, out_labels)
    recall_value = tp / total if total else 0.0
    return tp, total, recall_value


def _coverage_recall_counts(ground: list[str], output: list[str]) -> tuple[int, int]:
    ground_counter = Counter(ground)
    output_counter = Counter(output)
    tp = sum(min(ground_counter[key], output_counter.get(key, 0)) for key in ground_counter)
    total = sum(ground_counter.values())
    return tp, total


def _collect_stride_labels(items: list[dict[str, Any]]) -> list[str]:
    labels: list[str] = []
    for item in items:
        category = _normalize_stride(str(item.get("stride_category", "")).strip())
        if category:
            labels.append(category)
            continue

        frameworks = item.get("frameworks")
        if isinstance(frameworks, dict):
            for value in _coerce_string_list(frameworks.get("stride")):
                normalized = _normalize_stride(value)
                if normalized:
                    labels.append(normalized)
    return labels


def _collect_mitre_ids(items: list[dict[str, Any]]) -> list[str]:
    labels: list[str] = []
    for item in items:
        per_threat: set[str] = set()
        frameworks = item.get("frameworks")
        if isinstance(frameworks, dict):
            for value in _coerce_string_list(frameworks.get("mitreATT&CK")):
                normalized = _normalize_mitre_id(value)
                if normalized:
                    per_threat.add(normalized)

        references = item.get("references")
        if isinstance(references, list):
            for reference in references:
                if not isinstance(reference, str):
                    continue
                parsed = _extract_mitre_id_from_reference(reference)
                if parsed:
                    per_threat.add(parsed)

        for key in ("mitre_attack", "mitre_attack_id", "mitre", "mitreATT&CK"):
            for value in _coerce_string_list(item.get(key)):
                normalized = _normalize_mitre_id(value)
                if normalized:
                    per_threat.add(normalized)

        labels.extend(sorted(per_threat))

    return [label for label in labels if label]


def _coerce_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _extract_mitre_id_from_reference(reference: str) -> str | None:
    lowered = reference.lower()
    if "mitre" not in lowered:
        return None
    match = re.search(r"\bT\d{4}(?:\.\d{3})?\b", reference, flags=re.IGNORECASE)
    if not match:
        return None
    return _normalize_mitre_id(match.group(0))


def _normalize_mitre_id(value: str) -> str:
    text = value.strip().upper()
    match = re.search(r"\bT\d{4}(?:\.\d{3})?\b", text)
    if match:
        return match.group(0)
    return text
