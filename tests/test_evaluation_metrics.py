from threatcli.evaluation.metrics import ddr, hallucination_rate, precision, recall


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
