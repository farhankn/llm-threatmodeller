import json
from pathlib import Path
from types import SimpleNamespace

from threatcli.evaluation.runner import discover_fixtures, run_experiment


def test_discover_fixtures_finds_expected_cases() -> None:
    fixtures = discover_fixtures([Path("tests/fixtures")])
    fixture_names = {path.name for path in fixtures}
    assert "tri_01" in fixture_names
    assert "adv_01" in fixture_names


def test_run_experiment_writes_threat_logs_and_pairwise_jaccard(
    monkeypatch,
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "fixture_a"
    fixture.mkdir(parents=True)
    (fixture / "main.tf").write_text(
        'resource "aws_s3_bucket" "logs" { bucket = "logs-bucket" }\n',
        encoding="utf-8",
    )
    (fixture / "ground_truth.json").write_text(
        json.dumps(
            [
                {
                    "threat_id": "GT-1",
                    "stride_category": "Tampering",
                    "component": "aws_s3_bucket.logs",
                    "description": "x",
                    "discrepancy_flag": False,
                    "references": [],
                }
            ]
        ),
        encoding="utf-8",
    )

    calls = {"count": 0}

    def _fake_subprocess_run(command, capture_output, text, check):  # noqa: ANN001
        assert capture_output is True
        assert text is True
        assert check is False
        output_path = Path(command[command.index("--output") + 1])
        calls["count"] += 1
        if calls["count"] == 1:
            payload = [
                {
                    "threat_id": "OUT-1",
                    "stride_category": "Tampering",
                    "component": "aws_s3_bucket.logs",
                    "description": "x",
                    "discrepancy_flag": False,
                    "references": [],
                }
            ]
        else:
            payload = [
                {
                    "threat_id": "OUT-1",
                    "stride_category": "Tampering",
                    "component": "aws_s3_bucket.logs",
                    "description": "x",
                    "discrepancy_flag": False,
                    "references": [],
                },
                {
                    "threat_id": "OUT-2",
                    "stride_category": "Spoofing",
                    "component": "aws_s3_bucket.logs",
                    "description": "x",
                    "discrepancy_flag": False,
                    "references": [],
                },
            ]
        output_path.write_text(json.dumps(payload), encoding="utf-8")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr("threatcli.evaluation.runner.subprocess.run", _fake_subprocess_run)

    threat_log_dir = tmp_path / "logs"
    result = run_experiment(
        fixtures=[fixture],
        provider="openai",
        model=None,
        temperature=0.0,
        include_docs=False,
        repeats=2,
        threat_log_dir=threat_log_dir,
    )

    assert result["aggregate"]["pairwise_jaccard_pairs"] == 1
    assert result["aggregate"]["mean_pairwise_jaccard"] == 0.5
    assert result["pairwise_jaccard_by_fixture"][str(fixture)]["mean"] == 0.5

    logs = sorted(threat_log_dir.glob("*.json"))
    assert len(logs) == 2
    first_log = json.loads(logs[0].read_text(encoding="utf-8"))
    second_log = json.loads(logs[1].read_text(encoding="utf-8"))
    assert first_log["threat_count"] == 1
    assert second_log["threat_count"] == 2
