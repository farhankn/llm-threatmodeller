"""Core evaluation metrics used in Phase 3/4 experiments."""

from __future__ import annotations

from dataclasses import dataclass


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

