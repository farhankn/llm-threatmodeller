"""Terraform IaC parser and ResourceMap extraction."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Sequence

import hcl2

SENSITIVE_TOKENS = ("password", "secret", "key", "token")
REDACTED_VALUE = "[REDACTED]"


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
