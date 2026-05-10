"""Core evaluation metrics used in Phase 3/4 experiments."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Any


@dataclass(frozen=True)
class ConfusionCounts:
    tp: int
    fp: int
    fn: int


def precision(tp: int, fp: int) -> float:
    denominator = tp + fp
    if denominator == 0:
        return 0.0
    return tp / denominator


def recall(tp: int, fn: int) -> float:
    denominator = tp + fn
    if denominator == 0:
        return 0.0
    return tp / denominator


def ddr(matched_discrepancies: int, planted_discrepancies: int) -> float:
    if planted_discrepancies == 0:
        return 0.0
    return matched_discrepancies / planted_discrepancies


def hallucination_rate(hallucinated_count: int, total_output_count: int) -> float:
    if total_output_count == 0:
        return 0.0
    return hallucinated_count / total_output_count


def compute_jaccard(list_a: list[dict[str, Any]], list_b: list[dict[str, Any]]) -> float:
    """Compute Jaccard index across threat identity sets."""
    set_a = _threat_identity_set(list_a)
    set_b = _threat_identity_set(list_b)
    union = set_a | set_b
    if not union:
        return 1.0
    return len(set_a & set_b) / len(union)


def compute_pairwise_jaccard(runs: list[list[dict[str, Any]]]) -> dict[str, Any]:
    """Compute pairwise Jaccard stats and matrix for repeated runs."""
    count = len(runs)
    if count == 0:
        return {
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0,
            "n_pairs": 0,
            "matrix": [],
            "pair_scores": [],
        }

    matrix: list[list[float]] = [[1.0 if i == j else 0.0 for j in range(count)] for i in range(count)]
    pair_scores: list[float] = []
    for left_index in range(count):
        for right_index in range(left_index + 1, count):
            score = compute_jaccard(runs[left_index], runs[right_index])
            matrix[left_index][right_index] = score
            matrix[right_index][left_index] = score
            pair_scores.append(score)

    if pair_scores:
        return {
            "mean": float(mean(pair_scores)),
            "std": float(pstdev(pair_scores)),
            "min": min(pair_scores),
            "max": max(pair_scores),
            "n_pairs": len(pair_scores),
            "matrix": matrix,
            "pair_scores": pair_scores,
        }

    return {
        "mean": 1.0,
        "std": 0.0,
        "min": 1.0,
        "max": 1.0,
        "n_pairs": 0,
        "matrix": matrix,
        "pair_scores": [],
    }


def _threat_identity_set(threats: list[dict[str, Any]]) -> set[tuple[str, str]]:
    identities: set[tuple[str, str]] = set()
    for threat in threats:
        if not isinstance(threat, dict):
            continue
        component = str(threat.get("component", "")).strip().lower()
        category = str(threat.get("stride_category") or threat.get("category") or "").strip().lower()
        if component and category:
            identities.add((component, category))
    return identities
