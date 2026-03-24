import json
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from threatcli.cli import REQUIRED_THREAT_FIELDS, app

FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


class _FakeLLMClient:
    def __init__(self, payload: list[dict[str, Any]]):
        self._payload = payload

    def validate(self) -> None:
        return None

    def generate(self, prompt: dict[str, str], temperature: float = 0.5) -> str:
        assert "Infrastructure Summary" in prompt["user"]
        return json.dumps(self._payload)


def _load_ground_truth(case_id: str) -> list[dict[str, Any]]:
    path = FIXTURES_ROOT / case_id / "ground_truth.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("case_id", "expected_categories", "expected_component"),
    [
        ("tri_01", {"Information Disclosure"}, "aws_s3_bucket.public_bucket"),
        ("tri_02", {"Elevation of Privilege"}, "aws_security_group.ssh_open"),
        ("tri_03", {"Information Disclosure", "Tampering"}, "aws_db_instance.app_db"),
        ("tri_04", {"Elevation of Privilege"}, "aws_iam_policy.wildcard_admin"),
        ("tri_05", {"Information Disclosure"}, "aws_lambda_function.handler"),
    ],
)
def test_trivial_scenario_pipeline_with_mocked_llm(
    monkeypatch: pytest.MonkeyPatch,
    case_id: str,
    expected_categories: set[str],
    expected_component: str,
) -> None:
    ground_truth = _load_ground_truth(case_id)

    monkeypatch.setattr(
        "threatcli.cli.get_llm_client",
        lambda _provider, **_kwargs: _FakeLLMClient(ground_truth),
    )

    runner = CliRunner()
    tf_path = str(FIXTURES_ROOT / case_id / "main.tf")

    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            tf_path,
            "--format",
            "json",
            "--provider",
            "openai",
        ],
    )

    assert result.exit_code == 0, result.stdout

    output_threats = json.loads(result.stdout)
    assert isinstance(output_threats, list)
    assert output_threats

    for threat in output_threats:
        missing = REQUIRED_THREAT_FIELDS - set(threat.keys())
        assert not missing

    categories = {threat["stride_category"] for threat in output_threats}
    components = {threat["component"] for threat in output_threats}

    assert expected_categories.issubset(categories)
    assert expected_component in components


def test_analyze_nonexistent_path_returns_non_zero() -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["analyze", "--iac", "tests/fixtures/does_not_exist/main.tf", "--format", "json"],
    )

    assert result.exit_code != 0
    assert "Path does not exist" in result.output
