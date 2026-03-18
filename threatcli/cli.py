"""CLI entry point."""

from pathlib import Path

import typer

app = typer.Typer(help="Threat modeling CLI for IaC analysis.")


@app.command()
def analyze(
    iac: Path = typer.Option(..., "--iac", help="Path to Terraform file or directory."),
    format: str = typer.Option("text", "--format", help="Output format: text|json."),
    output: Path | None = typer.Option(None, "--output", help="Output file path for json format."),
    provider: str = typer.Option("openai", "--provider", help="LLM provider name."),
) -> None:
    """Analyze infrastructure and generate threats."""
    typer.echo(
        "Implementation in progress: analyze pipeline not fully wired yet. "
        f"iac={iac} format={format} output={output} provider={provider}"
    )


def main() -> None:
    """Run the Typer app."""
    app()
