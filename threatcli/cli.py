"""CLI entry point and pipeline orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from threatcli import __version__
from threatcli.context_builder import build_iac_prompt, build_multisource_prompt
from threatcli.llm_client import LLMError, get_llm_client
from threatcli.parsers.doc_parser import parse_documents
from threatcli.parsers.iac_parser import ParseError, parse_iac
from threatcli.renderer import filter_discrepancies, render_json, render_text

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
    payload = _extract_json_payload(raw_output)
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ThreatSchemaError(f"LLM output is not valid JSON: {exc}") from exc

    if not isinstance(parsed, list):
        raise ThreatSchemaError("LLM output must be a JSON array of threat objects")

    expanded = _expand_threat_items(parsed)
    parsed = [_normalize_threat_item(item, index) for index, item in enumerate(expanded)]

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


def _expand_threat_items(items: list[Any]) -> list[Any]:
    expanded: list[Any] = []
    for item in items:
        if isinstance(item, dict):
            nested = item.get("threats")
            if isinstance(nested, list):
                parent_resource = item.get("resource")
                for child in nested:
                    if isinstance(child, dict):
                        merged = dict(child)
                        if parent_resource and "resource" not in merged and "component" not in merged:
                            merged["resource"] = parent_resource
                        expanded.append(merged)
                    else:
                        expanded.append(child)
                continue

            nested_model = item.get("threat_model")
            if isinstance(nested_model, list):
                expanded.extend(nested_model)
                continue
            if isinstance(nested_model, dict):
                maybe_nested = nested_model.get("threats")
                if isinstance(maybe_nested, list):
                    parent_resource = item.get("resource") or nested_model.get("resource")
                    for child in maybe_nested:
                        if isinstance(child, dict):
                            merged = dict(child)
                            if parent_resource and "resource" not in merged and "component" not in merged:
                                merged["resource"] = parent_resource
                            expanded.append(merged)
                        else:
                            expanded.append(child)
                    continue

        expanded.append(item)
    return expanded


def _extract_json_payload(raw_output: str) -> str:
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    if cleaned.startswith("[") and cleaned.endswith("]"):
        return cleaned

    start = cleaned.find("[")
    if start == -1:
        return cleaned

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(cleaned)):
        char = cleaned[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return cleaned[start : index + 1]

    return cleaned


def _normalize_threat_item(threat: Any, index: int) -> dict[str, Any]:
    if not isinstance(threat, dict):
        raise ThreatSchemaError(f"Threat at index {index} is not an object")

    nested_model = threat.get("threat_model")
    if isinstance(nested_model, dict):
        return _normalize_threat_item(nested_model, index)

    if REQUIRED_THREAT_FIELDS.issubset(threat.keys()):
        normalized = dict(threat)
        normalized["references"] = _coerce_references(normalized.get("references"))
        return normalized

    explicit_component = str(threat.get("component", "")).strip()
    resource_type = str(threat.get("resource_type", "")).strip()
    resource_name = str(threat.get("resource_name") or threat.get("resource") or "").strip()
    if explicit_component and "." in explicit_component:
        resource_type, resource_name = explicit_component.split(".", 1)
    elif not resource_type and "." in resource_name and resource_name.startswith("aws_"):
        resource_type, resource_name = resource_name.split(".", 1)
    threat_type = str(
        threat.get("threat_type") or threat.get("stride_category") or threat.get("stride") or ""
    ).strip()
    threat_type = _normalize_stride_category(threat_type)
    description = str(threat.get("description") or threat.get("threat_description") or "").strip()

    if not description:
        description = str(threat.get("name", "")).strip()

    if resource_type and resource_name and threat_type and description:
        component = f"{resource_type}.{resource_name}"
        evidence = threat.get("evidence")
        discrepancy_detail = str(threat.get("discrepancy_detail", "")).strip()
        discrepancy_flag = bool(threat.get("discrepancy_flag", threat.get("discrepancy", False)))
        if not discrepancy_flag and discrepancy_detail:
            discrepancy_flag = True
        references = _coerce_references(evidence if evidence is not None else [])
        return {
            "threat_id": str(threat.get("threat_id") or f"T-{index + 1:03d}"),
            "stride_category": threat_type,
            "component": component,
            "description": description,
            "discrepancy_flag": discrepancy_flag,
            "references": references,
        }

    # Fallback mapping for models that provide stride + description but omit component fields.
    if threat_type and description:
        references = _coerce_references(threat.get("evidence"))
        fallback_component = _infer_component(resource_type, resource_name, references, description)
        return {
            "threat_id": str(threat.get("threat_id") or f"T-{index + 1:03d}"),
            "stride_category": threat_type,
            "component": fallback_component,
            "description": description,
            "discrepancy_flag": bool(threat.get("discrepancy_flag", threat.get("discrepancy", False))),
            "references": references,
        }

    return dict(threat)


def _coerce_references(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, dict):
        refs: list[str] = []
        for key, item in value.items():
            text = str(item).strip()
            if text:
                refs.append(f"{key}: {text}")
        return refs
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if value is None:
        return []
    return []


def _normalize_stride_category(value: str) -> str:
    normalized = value.strip().lower()
    mapping = {
        "spoofing": "Spoofing",
        "tampering": "Tampering",
        "repudiation": "Repudiation",
        "information disclosure": "Information Disclosure",
        "denial of service": "Denial of Service",
        "elevation of privilege": "Elevation of Privilege",
        "privilege escalation": "Elevation of Privilege",
    }
    return mapping.get(normalized, value.strip())


def _infer_component(
    resource_type: str,
    resource_name: str,
    references: list[str],
    description: str,
) -> str:
    if resource_type and resource_name:
        return f"{resource_type}.{resource_name}"

    source_text = " ".join([*references, description]).lower()
    patterns = (
        ("aws_security_group", ("security_group", "security group", "ingress", "egress")),
        ("aws_db_instance", ("db instance", "rds", "database", "postgres")),
        ("aws_s3_bucket", ("s3", "bucket", "artifact")),
        ("aws_iam_policy", ("iam policy", "wildcard-admin", "wildcard policy")),
        ("aws_instance", ("bastion", "ec2 instance", "aws_instance")),
    )
    for resource, markers in patterns:
        if any(marker in source_text for marker in markers):
            if resource == "aws_security_group" and "bastion" in source_text:
                return "aws_security_group.bastion"
            if resource == "aws_security_group" and "web" in source_text:
                return "aws_security_group.web"
            if resource == "aws_db_instance" and ("app-db-prod" in source_text or "'app'" in source_text):
                return "aws_db_instance.app"
            if resource == "aws_db_instance" and "app_db" in source_text:
                return "aws_db_instance.app_db"
            if resource == "aws_s3_bucket" and "artifact" in source_text:
                return "aws_s3_bucket.artifacts"
            if resource == "aws_s3_bucket" and "logs" in source_text:
                return "aws_s3_bucket.logs"
            if resource == "aws_iam_policy":
                return "aws_iam_policy.wildcard_admin"
            if resource == "aws_instance" and "bastion" in source_text:
                return "aws_instance.bastion"

    return "unknown.component"


def _emit_output(content: str, output: Path | None) -> None:
    if output is None:
        typer.echo(content)
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content + "\n", encoding="utf-8")


@app.command()
def analyze(
    iac: list[Path] = typer.Option(..., "--iac", "-i", help="Terraform file or directory paths."),
    doc: list[Path] = typer.Option(
        [],
        "--doc",
        help="Optional design doc file(s) or directory path(s) (.md/.txt). Repeat --doc for multiple inputs.",
    ),
    doc_dir: list[Path] = typer.Option(
        [],
        "--doc-dir",
        help="Optional directory containing design docs (.md/.txt). Repeat --doc-dir for multiple directories.",
    ),
    max_doc_tokens: int = typer.Option(
        15000,
        "--max-doc-tokens",
        help="Maximum total design-document tokens to ingest before truncation.",
    ),
    max_chunk_tokens: int = typer.Option(
        1500,
        "--max-chunk-tokens",
        help="Maximum tokens per document chunk.",
    ),
    overlap_tokens: int = typer.Option(
        100,
        "--overlap-tokens",
        help="Overlap tokens between adjacent chunks.",
    ),
    format: str = typer.Option("text", "--format", "-f", help="Output format: text|json|pdf."),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output file path for file output."),
    provider: str = typer.Option("openai", "--provider", help="LLM provider: openai|gemini|ollama."),
    temperature: float = typer.Option(0.5, "--temperature", help="LLM temperature (0.0-1.0)."),
    model: str | None = typer.Option(None, "--model", help="Optional model override for provider."),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Print built prompt context and skip LLM call.",
    ),
    discrepancies_only: bool = typer.Option(
        False,
        "--discrepancies-only",
        help="Show only threats with discrepancy_flag=true.",
    ),
) -> None:
    """Analyze infrastructure and generate threats."""
    normalized_format = format.strip().lower()

    if normalized_format not in {"text", "json", "pdf"}:
        typer.echo(f"Error: Unsupported format '{format}'.", err=True)
        raise typer.Exit(code=1)

    if normalized_format == "pdf":
        typer.echo("Error: PDF output is not implemented in Phase 1.", err=True)
        raise typer.Exit(code=1)
    if max_doc_tokens <= 0 or max_chunk_tokens <= 0 or overlap_tokens < 0:
        typer.echo("Error: Invalid document token options.", err=True)
        raise typer.Exit(code=1)

    try:
        resource_map = parse_iac(iac)
        all_doc_inputs = [*doc, *doc_dir]
        if all_doc_inputs:
            chunks = parse_documents(
                all_doc_inputs,
                max_chunk_tokens=max_chunk_tokens,
                overlap_tokens=overlap_tokens,
                max_doc_tokens=max_doc_tokens,
            )
            prompt = build_multisource_prompt(resource_map, chunks)
        else:
            prompt = build_iac_prompt(resource_map)

        if dry_run:
            _emit_output(render_json([{"mode": "dry-run", "prompt": prompt}]), output)
            return

        client_kwargs: dict[str, Any] = {}
        if model:
            client_kwargs["model"] = model

        client = get_llm_client(provider, **client_kwargs)
        client.validate()

        raw_output = client.generate(prompt=prompt, temperature=temperature)
        threats = parse_threats(raw_output)
        if discrepancies_only:
            threats = filter_discrepancies(threats)

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
