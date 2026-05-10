"""Terraform IaC parser and ResourceMap extraction."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Sequence

import hcl2

SENSITIVE_TOKENS = ("password", "secret", "key", "token")
REDACTED_VALUE = "[REDACTED]"
MAX_LIST_ITEMS = 10
MAX_STRING_LENGTH = 100
MAX_SUMMARY_CHARS = 8000


class ParseError(ValueError):
    """Raised when Terraform input cannot be parsed."""


def parse_iac(paths: Sequence[str | Path]) -> dict[str, Any]:
    """Parse Terraform inputs into a normalized ResourceMap."""
    files = discover_tf_files(paths)
    resource_map: dict[str, Any] = {
        "resources": [],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    for tf_file in files:
        parsed = _parse_file(tf_file)
        if parsed:
            _merge_into_resource_map(resource_map, parsed)

    resource_map["variables"] = sorted(set(resource_map["variables"]))
    return resource_map


def serialize_resource_map(resource_map: dict[str, Any], char_budget: int = MAX_SUMMARY_CHARS) -> str:
    """Serialize ResourceMap into a compact JSON summary for LLM prompts."""
    resources = [_summarize_resource(resource) for resource in resource_map.get("resources", [])]
    relationships = _infer_relationships(resource_map)
    
    summary = {
        "resources": resources,
        "relationships": relationships,
        "providers": [_summarize_value(provider) for provider in resource_map.get("providers", [])],
        "variables": _summarize_value(resource_map.get("variables", [])),
        "data_sources": [_summarize_resource(source) for source in resource_map.get("data_sources", [])],
        "modules": [_summarize_value(module) for module in resource_map.get("modules", [])],
    }

    text = json.dumps(summary, indent=2)
    if len(text) <= char_budget:
        return text

    # Truncate logic...
    summary["relationships"] = []
    summary["variables"] = []
    text = json.dumps(summary, indent=2)
    if len(text) <= char_budget:
        return text

    summary["modules"] = []
    text = json.dumps(summary, indent=2)
    if len(text) <= char_budget:
        return text

    summary["data_sources"] = []
    text = json.dumps(summary, indent=2)
    if len(text) <= char_budget:
        return text

    for resource in summary["resources"]:
        if isinstance(resource, dict):
            resource["attributes"] = "[omitted due to budget]"

    text = json.dumps(summary, indent=2)
    if len(text) <= char_budget:
        return text

    # Final safeguard: truncate by characters while preserving valid JSON string type.
    overflow = len(text) - char_budget
    return json.dumps({"summary": text[: char_budget - 32], "truncated_chars": overflow}, indent=2)


def _infer_relationships(resource_map: dict[str, Any]) -> list[str]:
    relationships = []
    resources = resource_map.get("resources", [])
    # Map of short names (name) to canonical identifiers (type.name)
    names_to_ids = {r['name']: f"{r['type']}.{r['name']}" for r in resources if 'name' in r and 'type' in r}
    
    for resource in resources:
        source_id = f"{resource['type']}.{resource['name']}"
        # Search attributes for references to other resource names
        attr_str = str(resource.get("attributes", {}))
        for short_name, target_id in names_to_ids.items():
            if short_name != resource['name'] and (f'"{short_name}"' in attr_str or f"'{short_name}'" in attr_str or f"={short_name}" in attr_str):
                relationships.append(f"{source_id} -> {target_id}")
    
    return sorted(list(set(relationships)))


def discover_tf_files(paths: Iterable[str | Path]) -> list[Path]:
    """Resolve files/directories to concrete `.tf` paths."""
    discovered: list[Path] = []
    seen: set[Path] = set()

    for raw_path in paths:
        path = Path(raw_path)

        if not path.exists():
            raise ParseError(f"Path does not exist: {path}")

        if path.is_dir():
            candidates = sorted(path.glob("**/*.tf"))
        else:
            candidates = [path] if path.suffix == ".tf" else []

        for candidate in candidates:
            absolute = candidate.resolve()
            if absolute not in seen:
                discovered.append(candidate)
                seen.add(absolute)

    return discovered


def _parse_file(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ParseError(f"Unable to read Terraform file '{path}': {exc}") from exc

    if not text.strip():
        return {}

    try:
        parsed = hcl2.loads(text)
    except Exception as exc:  # noqa: BLE001 - hcl2 parser raises mixed exception types
        raise ParseError(f"Failed to parse Terraform file '{path}': {exc}") from exc

    if not isinstance(parsed, dict):
        raise ParseError(f"Unexpected parse output for '{path}': expected object")

    return _redact_sensitive_values(parsed)


def _merge_into_resource_map(resource_map: dict[str, Any], parsed: dict[str, Any]) -> None:
    _extract_resources(resource_map, parsed.get("resource", []))
    _extract_providers(resource_map, parsed.get("provider", []))
    _extract_variables(resource_map, parsed.get("variable", []))
    _extract_data_sources(resource_map, parsed.get("data", []))
    _extract_modules(resource_map, parsed.get("module", []))


def _extract_resources(resource_map: dict[str, Any], blocks: Any) -> None:
    for block in _as_list(blocks):
        if not isinstance(block, dict):
            continue
        for resource_type, instances in block.items():
            if not isinstance(instances, dict):
                continue
            for name, attributes in instances.items():
                resource_map["resources"].append(
                    {
                        "type": resource_type,
                        "name": name,
                        "attributes": attributes if isinstance(attributes, dict) else {},
                    }
                )


def _extract_providers(resource_map: dict[str, Any], blocks: Any) -> None:
    for block in _as_list(blocks):
        if not isinstance(block, dict):
            continue
        for name, attributes in block.items():
            provider: dict[str, Any] = {"name": name}
            if isinstance(attributes, dict):
                provider.update(attributes)
            resource_map["providers"].append(provider)


def _extract_variables(resource_map: dict[str, Any], blocks: Any) -> None:
    for block in _as_list(blocks):
        if not isinstance(block, dict):
            continue
        resource_map["variables"].extend(block.keys())


def _extract_data_sources(resource_map: dict[str, Any], blocks: Any) -> None:
    for block in _as_list(blocks):
        if not isinstance(block, dict):
            continue
        for data_type, instances in block.items():
            if not isinstance(instances, dict):
                continue
            for name, attributes in instances.items():
                resource_map["data_sources"].append(
                    {
                        "type": data_type,
                        "name": name,
                        "attributes": attributes if isinstance(attributes, dict) else {},
                    }
                )


def _extract_modules(resource_map: dict[str, Any], blocks: Any) -> None:
    for block in _as_list(blocks):
        if not isinstance(block, dict):
            continue
        for name, attributes in block.items():
            module: dict[str, Any] = {"name": name}
            if isinstance(attributes, dict):
                module.update(attributes)
            resource_map["modules"].append(module)


def _summarize_resource(resource: Any) -> dict[str, Any]:
    if not isinstance(resource, dict):
        return {}

    return {
        "type": resource.get("type"),
        "name": resource.get("name"),
        "attributes": _summarize_value(resource.get("attributes", {})),
    }


def _summarize_value(value: Any) -> Any:
    if value == REDACTED_VALUE:
        return REDACTED_VALUE

    if isinstance(value, dict):
        if _looks_like_policy(value):
            statements = value.get("Statement", [])
            statement_count = len(statements) if isinstance(statements, list) else 0
            return f"[inline policy, {statement_count} statements]"

        if len(value) > MAX_LIST_ITEMS:
            return f"[inline JSON, {len(value)} keys]"

        result: dict[str, Any] = {}
        for key, nested in value.items():
            summarized = _summarize_value(nested)
            if summarized is not None:
                result[key] = summarized
        return result

    if isinstance(value, list):
        items = [_summarize_value(item) for item in value]
        compact_items = [item for item in items if item is not None]
        if len(compact_items) <= MAX_LIST_ITEMS:
            return compact_items

        remaining = len(compact_items) - MAX_LIST_ITEMS
        return compact_items[:MAX_LIST_ITEMS] + [f"...and {remaining} more"]

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        if len(value) <= MAX_STRING_LENGTH:
            return value
        return f"[string, {len(value)} chars]"

    return None


def _looks_like_policy(value: dict[str, Any]) -> bool:
    lowered = {key.lower() for key in value}
    return "statement" in lowered and "version" in lowered


def _redact_sensitive_values(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, nested in value.items():
            if _looks_sensitive(key):
                redacted[key] = REDACTED_VALUE
            else:
                redacted[key] = _redact_sensitive_values(nested)
        return redacted

    if isinstance(value, list):
        return [_redact_sensitive_values(item) for item in value]

    return value


def _looks_sensitive(key: str) -> bool:
    lowered = key.lower()
    return any(token in lowered for token in SENSITIVE_TOKENS)


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []
