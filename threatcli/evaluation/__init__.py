"""Evaluation utilities for experiment scoring and comparisons."""

from threatcli.evaluation.comparator import compare, load_ground_truth, load_llm_output
from threatcli.evaluation.acse_importer import (
    hydrate_records_from_hf_paths,
    import_acse_records,
    load_dataset_records,
)
from threatcli.evaluation.metrics import (
    ConfusionCounts,
    compute_jaccard,
    compute_pairwise_jaccard,
    ddr,
    hallucination_rate,
    precision,
    recall,
)
from threatcli.evaluation.runner import discover_fixtures, run_experiment, write_run_result

__all__ = [
    "ConfusionCounts",
    "compare",
    "compute_jaccard",
    "compute_pairwise_jaccard",
    "ddr",
    "discover_fixtures",
    "hallucination_rate",
    "hydrate_records_from_hf_paths",
    "import_acse_records",
    "load_dataset_records",
    "load_ground_truth",
    "load_llm_output",
    "precision",
    "recall",
    "run_experiment",
    "write_run_result",
]
