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
