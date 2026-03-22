import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from threatcli.cli import app

FIXTURE_FILE = Path(__file__).resolve().parents[1] / "fixtures" / "tri_01" / "main.tf"


class _FakeLLMClient:
    def validate(self) -> None:
        return None

    def generate(self, prompt: dict[str, str], temperature: float = 0.5) -> str:
        assert "Infrastructure Summary" in prompt["user"]
        return json.dumps(
            [
                {
                    "threat_id": "T-001",
                    "stride_category": "Information Disclosure",
                    "component": "aws_s3_bucket.public_bucket",
                    "description": "Public bucket ACL allows unauthenticated reads.",
                    "discrepancy_flag": False,
                    "discrepancy_detail": "",
                    "severity": "High",
                    "references": ["aws_s3_bucket.public_bucket.acl = \"public-read\""]
                }
            ]
        )


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_smoke_text_output(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    monkeypatch.setattr("threatcli.cli.get_llm_client", lambda _provider, **_kwargs: _FakeLLMClient())

    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            str(FIXTURE_FILE),
            "--format",
            "text",
            "--provider",
            "openai",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert "Information Disclosure" in result.stdout
    assert "aws_s3_bucket.public_bucket" in result.stdout


def test_smoke_json_output_file(
    monkeypatch: pytest.MonkeyPatch,
    runner: CliRunner,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr("threatcli.cli.get_llm_client", lambda _provider, **_kwargs: _FakeLLMClient())

    out_file = tmp_path / "threats.json"
    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            str(FIXTURE_FILE),
            "--format",
            "json",
            "--output",
            str(out_file),
            "--provider",
            "openai",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert out_file.exists()

    threats = json.loads(out_file.read_text(encoding="utf-8"))
    assert isinstance(threats, list)
    assert threats[0]["stride_category"] == "Information Disclosure"


def test_help_command(runner: CliRunner) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
