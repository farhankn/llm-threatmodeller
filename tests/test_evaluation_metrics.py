from threatcli.evaluation.metrics import (
    compute_jaccard,
    compute_pairwise_jaccard,
    ddr,
    hallucination_rate,
    precision,
    recall,
)


def test_precision() -> None:
    assert precision(8, 2) == 0.8
    assert precision(0, 0) == 0.0


def test_recall() -> None:
    assert recall(7, 3) == 0.7
    assert recall(0, 0) == 0.0


def test_ddr() -> None:
    assert ddr(3, 4) == 0.75
    assert ddr(0, 0) == 0.0


def test_hallucination_rate() -> None:
    assert hallucination_rate(1, 10) == 0.1
    assert hallucination_rate(0, 0) == 0.0


def test_compute_jaccard() -> None:
    run_a = [
        {"stride_category": "Tampering", "component": "aws_s3_bucket.logs"},
        {"stride_category": "Spoofing", "component": "aws_iam_role.app"},
    ]
    run_b = [
        {"stride_category": "Tampering", "component": "aws_s3_bucket.logs"},
        {"stride_category": "Denial of Service", "component": "aws_lambda_function.api"},
    ]
    assert compute_jaccard(run_a, run_b) == 1 / 3


def test_compute_jaccard_handles_two_empty_runs() -> None:
    assert compute_jaccard([], []) == 1.0


def test_compute_pairwise_jaccard() -> None:
    runs = [
        [
            {"stride_category": "Tampering", "component": "aws_s3_bucket.logs"},
            {"stride_category": "Spoofing", "component": "aws_iam_role.app"},
        ],
        [
            {"stride_category": "Tampering", "component": "aws_s3_bucket.logs"},
        ],
        [
            {"stride_category": "Information Disclosure", "component": "aws_db_instance.app"},
        ],
    ]
    result = compute_pairwise_jaccard(runs)
    assert result["n_pairs"] == 3
    assert result["min"] == 0.0
    assert result["max"] == 0.5
    assert len(result["matrix"]) == 3
    assert result["matrix"][0][0] == 1.0


def test_compute_pairwise_jaccard_single_run() -> None:
    result = compute_pairwise_jaccard(
        [[{"stride_category": "Tampering", "component": "aws_s3_bucket.logs"}]]
    )
    assert result["n_pairs"] == 0
    assert result["mean"] == 1.0
    assert result["matrix"] == [[1.0]]
