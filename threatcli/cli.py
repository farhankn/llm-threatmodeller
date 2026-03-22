"""CLI entry point and pipeline orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from threatcli import __version__
from threatcli.context_builder import build_iac_prompt
from threatcli.llm_client import LLMError, get_llm_client
from threatcli.parsers.iac_parser import ParseError, parse_iac
from threatcli.renderer import render_json, render_text

app = typer.Typer(help="Threat modeling CLI for IaC analysis.")

REQUIRED_THREAT_FIELDS = {
    "threat_id",
    "stride_category",
    "component",
    "description",
    "discrepancy_flag",
    "references",
}


class ThreatSchemaError(ValueError):
    """Raised when model output does not conform to expected threat schema."""


def parse_threats(raw_output: str) -> list[dict[str, Any]]:
    """Parse and validate threat array from LLM response."""
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise ThreatSchemaError(f"LLM output is not valid JSON: {exc}") from exc

    if not isinstance(parsed, list):
        raise ThreatSchemaError("LLM output must be a JSON array of threat objects")

    for index, threat in enumerate(parsed):
        if not isinstance(threat, dict):
            raise ThreatSchemaError(f"Threat at index {index} is not an object")

        missing = REQUIRED_THREAT_FIELDS - set(threat.keys())
        if missing:
            missing_keys = ", ".join(sorted(missing))
            raise ThreatSchemaError(f"Threat at index {index} missing required keys: {missing_keys}")

        if not isinstance(threat.get("references"), list):
            raise ThreatSchemaError(f"Threat at index {index} field 'references' must be an array")

    return parsed


def _emit_output(content: str, output: Path | None) -> None:
    if output is None:
        typer.echo(content)
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content + "\n", encoding="utf-8")


@app.command()
def analyze(
    iac: list[Path] = typer.Option(..., "--iac", "-i", help="Terraform file or directory paths."),
    format: str = typer.Option("text", "--format", "-f", help="Output format: text|json|pdf."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output file path for file output."),
    provider: str = typer.Option("openai", "--provider", help="LLM provider: openai|gemini|ollama."),
    temperature: float = typer.Option(0.5, "--temperature", help="LLM temperature (0.0-1.0)."),
    model: str | None = typer.Option(None, "--model", help="Optional model override for provider."),
) -> None:
    """Analyze infrastructure and generate threats."""
    normalized_format = format.strip().lower()

    if normalized_format not in {"text", "json", "pdf"}:
        typer.echo(f"Error: Unsupported format '{format}'.", err=True)
        raise typer.Exit(code=1)

    if normalized_format == "pdf":
        typer.echo("Error: PDF output is not implemented in Phase 1.", err=True)
        raise typer.Exit(code=1)

    try:
        resource_map = parse_iac(iac)
        prompt = build_iac_prompt(resource_map)

        client_kwargs: dict[str, Any] = {}
        if model:
            client_kwargs["model"] = model

        client = get_llm_client(provider, **client_kwargs)
        client.validate()

        raw_output = client.generate(prompt=prompt, temperature=temperature)
        threats = parse_threats(raw_output)

        rendered = render_text(threats) if normalized_format == "text" else render_json(threats)
        _emit_output(rendered, output)
    except (ParseError, LLMError, ThreatSchemaError, OSError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


@app.command()
def validate(
    iac: list[Path] = typer.Option(..., "--iac", "-i", help="Terraform file or directory paths."),
) -> None:
    """Validate Terraform files are parseable."""
    try:
        parse_iac(iac)
    except ParseError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo("Validation successful.")


@app.command()
def version(
    provider: str = typer.Option("openai", "--provider", help="Provider to display in version output."),
) -> None:
    """Print version and selected provider."""
    typer.echo(f"threatcli {__version__} (provider: {provider})")


def main() -> None:
    """Run the Typer app."""
    app()
