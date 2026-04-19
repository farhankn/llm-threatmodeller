"""Import ACSE-Eval-like records into local fixture directories."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import requests

REQUIRED_THREAT_FIELDS = {
    "threat_id",
    "stride_category",
    "component",
    "description",
    "discrepancy_flag",
    "references",
}


def load_dataset_records(dataset_path: Path) -> list[dict[str, Any]]:
    if dataset_path.suffix.lower() == ".parquet":
        return _load_parquet_records(dataset_path)

    text = dataset_path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if dataset_path.suffix.lower() == ".jsonl":
        records: list[dict[str, Any]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                records.append(parsed)
        return records

    parsed = json.loads(text)
    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)]
    if isinstance(parsed, dict):
        # supports HuggingFace export-like structure: {"train":[...], "test":[...]}
        if "train" in parsed and isinstance(parsed["train"], list):
            return [item for item in parsed["train"] if isinstance(item, dict)]
        return [parsed]
    return []


def _load_parquet_records(dataset_path: Path) -> list[dict[str, Any]]:
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover - environment-dependent dependency
        raise ValueError(
            "Parquet support requires 'pyarrow'. Install it with: pip install pyarrow"
        ) from exc
    table = pq.read_table(dataset_path)
    rows = table.to_pylist()
    return [item for item in rows if isinstance(item, dict)]


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_").lower()
    return slug or "scenario"


def _coerce_references(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, dict):
        refs: list[str] = []
        for key, item in value.items():
            text = str(item).strip()
            if text:
                refs.append(f"{key}: {text}")
        return refs
    return []


def _normalize_stride(value: str) -> str:
    normalized = value.strip().lower()
    aliases = {
        "privilege escalation": "Elevation of Privilege",
        "elevation of privilege": "Elevation of Privilege",
        "information disclosure": "Information Disclosure",
        "denial of service": "Denial of Service",
        "spoofing": "Spoofing",
        "tampering": "Tampering",
        "repudiation": "Repudiation",
    }
    return aliases.get(normalized, value.strip() or "Tampering")


def normalize_threat_item(item: dict[str, Any], index: int) -> dict[str, Any]:
    component = str(
        item.get("component") or item.get("resource") or item.get("asset") or "unknown.component"
    ).strip()
    description = str(
        item.get("description") or item.get("threat_description") or item.get("summary") or item.get("name") or ""
    ).strip()
    if not description:
        description = "Threat imported from ACSE-Eval dataset."
    stride = _normalize_stride(
        str(item.get("stride_category") or item.get("stride") or item.get("category") or item.get("threat_type") or "")
    )
    threat_id = str(item.get("threat_id") or item.get("id") or f"ACSE-{index + 1:03d}")
    discrepancy_flag = bool(item.get("discrepancy_flag", item.get("discrepancy", False)))
    references = _coerce_references(item.get("references") if item.get("references") is not None else item.get("evidence"))
    return {
        "threat_id": threat_id,
        "stride_category": stride,
        "component": component,
        "description": description,
        "discrepancy_flag": discrepancy_flag,
        "references": references,
    }


def extract_ground_truth(record: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = [
        record.get("ground_truth"),
        record.get("threats"),
        record.get("expected_threats"),
    ]
    threat_model = record.get("threat_model")
    if isinstance(threat_model, list):
        candidates.append(threat_model)
    elif isinstance(threat_model, dict):
        nested = threat_model.get("threats")
        if isinstance(nested, list):
            candidates.append(nested)
        else:
            candidates.append([threat_model])

    for candidate in candidates:
        if isinstance(candidate, list) and candidate:
            normalized: list[dict[str, Any]] = []
            for idx, item in enumerate(candidate):
                if isinstance(item, dict):
                    normalized.append(normalize_threat_item(item, idx))
            if normalized:
                return normalized

    # Fallback: treat top-level record as one threat if it resembles threat fields.
    if REQUIRED_THREAT_FIELDS.intersection(record.keys()):
        return [normalize_threat_item(record, 0)]
    return []


def _select_text(record: dict[str, Any], keys: tuple[str, ...], fallback: str) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return fallback


def hydrate_records_from_hf_paths(
    records: list[dict[str, Any]],
    repo_id: str = "ACSE-Eval/ACSE-Eval",
    timeout_seconds: float = 20.0,
) -> list[dict[str, Any]]:
    hydrated: list[dict[str, Any]] = []
    for record in records:
        enriched = dict(record)
        threat_model_path = str(enriched.get("threat_model") or "").strip()
        architecture_description_path = str(enriched.get("architecture_description") or "").strip()
        infra_path = str(enriched.get("infra_as_code") or "").strip()

        if threat_model_path:
            url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{threat_model_path}"
            try:
                response = requests.get(url, timeout=timeout_seconds)
                response.raise_for_status()
                parsed = response.json()
                if isinstance(parsed, list):
                    enriched["ground_truth"] = parsed
                elif isinstance(parsed, dict):
                    if isinstance(parsed.get("threats"), list):
                        enriched["ground_truth"] = parsed["threats"]
                    else:
                        enriched["ground_truth"] = [parsed]
            except (requests.RequestException, json.JSONDecodeError):
                pass

        if architecture_description_path and not enriched.get("design_doc"):
            url = (
                f"https://huggingface.co/datasets/{repo_id}/resolve/main/{architecture_description_path}"
            )
            try:
                response = requests.get(url, timeout=timeout_seconds)
                response.raise_for_status()
                enriched["design_doc"] = response.text
            except requests.RequestException:
                pass

        if infra_path and not enriched.get("terraform"):
            enriched["terraform"] = (
                f"# ACSE-Eval IaC source path (dataset-relative):\n# {infra_path}\n"
                "# Pull IaC files from dataset repository and replace this placeholder.\n"
            )

        hydrated.append(enriched)
    return hydrated


def import_acse_records(records: list[dict[str, Any]], output_root: Path, prefix: str = "acse") -> dict[str, int]:
    imported = 0
    skipped = 0
    output_root.mkdir(parents=True, exist_ok=True)

    for index, record in enumerate(records, start=1):
        scenario_name = _slugify(str(record.get("id") or record.get("scenario_id") or f"{prefix}_{index:03d}"))
        fixture_dir = output_root / scenario_name
        ground_truth = extract_ground_truth(record)
        if not ground_truth:
            skipped += 1
            continue

        fixture_dir.mkdir(parents=True, exist_ok=True)
        terraform_text = _select_text(
            record,
            ("terraform", "iac", "iac_code", "infra", "code"),
            "# TODO: replace with Terraform extracted from ACSE record\n",
        )
        design_text = _select_text(
            record,
            ("design_doc", "design", "architecture", "context", "system_description"),
            "Imported from ACSE-Eval record.\n",
        )

        (fixture_dir / "main.tf").write_text(terraform_text.rstrip() + "\n", encoding="utf-8")
        (fixture_dir / "design.md").write_text(design_text.rstrip() + "\n", encoding="utf-8")
        (fixture_dir / "ground_truth.json").write_text(
            json.dumps(ground_truth, indent=2) + "\n",
            encoding="utf-8",
        )
        (fixture_dir / "source_record.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        imported += 1

    return {"imported": imported, "skipped": skipped}
