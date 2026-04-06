import json

from typer.testing import CliRunner

from threatcli.cli import app


def test_help_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_analyze_dry_run_outputs_prompt_json() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            "tests/fixtures/tri_01/main.tf",
            "--dry-run",
            "--format",
            "json",
        ],
    )
    assert result.exit_code == 0
    assert '"mode": "dry-run"' in result.stdout
    assert "Infrastructure Summary" in result.stdout


def test_analyze_dry_run_accepts_multiple_doc_inputs(tmp_path) -> None:
    doc_a = tmp_path / "a.md"
    doc_b = tmp_path / "b.txt"
    doc_a.write_text("# A\narchitecture text", encoding="utf-8")
    doc_b.write_text("security text", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            "tests/fixtures/tri_01/main.tf",
            "--doc",
            str(doc_a),
            "--doc",
            str(doc_b),
            "--dry-run",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    assert "Design Document Context" in result.stdout


def test_discrepancies_only_filters_output(monkeypatch) -> None:
    class _FakeLLMClient:
        def validate(self) -> None:
            return None

        def generate(self, prompt: dict[str, str], temperature: float = 0.5) -> str:
            return json.dumps(
                [
                    {
                        "threat_id": "T-1",
                        "stride_category": "Information Disclosure",
                        "component": "aws_s3_bucket.logs",
                        "description": "public logs",
                        "discrepancy_flag": True,
                        "references": ["r1"],
                    },
                    {
                        "threat_id": "T-2",
                        "stride_category": "Tampering",
                        "component": "aws_db_instance.app",
                        "description": "db issue",
                        "discrepancy_flag": False,
                        "references": ["r2"],
                    },
                ]
            )

    monkeypatch.setattr("threatcli.cli.get_llm_client", lambda _provider, **_kwargs: _FakeLLMClient())

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            "tests/fixtures/adv_01/main.tf",
            "--doc",
            "tests/fixtures/adv_01/design.md",
            "--discrepancies-only",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 1
    assert data[0]["threat_id"] == "T-1"


def test_analyze_dry_run_accepts_doc_dir_input() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            "tests/fixtures/adv_02/main.tf",
            "--doc-dir",
            "tests/fixtures/adv_02",
            "--dry-run",
            "--format",
            "json",
        ],
    )
    assert result.exit_code == 0
    assert "Design Document Context" in result.stdout


def test_analyze_rejects_invalid_doc_token_options() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "--iac",
            "tests/fixtures/tri_01/main.tf",
            "--max-doc-tokens",
            "0",
            "--dry-run",
            "--format",
            "json",
        ],
    )
    assert result.exit_code != 0
    assert "Invalid document token options" in result.output
