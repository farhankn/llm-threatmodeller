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


def _extract_stride_categories(item: dict[str, Any]) -> list[str]:
    # ACSE source records often store STRIDE under frameworks.stride as a multi-label list.
    frameworks = item.get("frameworks")
    if isinstance(frameworks, dict):
        stride_values = frameworks.get("stride")
        if isinstance(stride_values, list):
            categories = [_normalize_stride(str(value)) for value in stride_values if str(value).strip()]
            if categories:
                return categories
        if isinstance(stride_values, str) and stride_values.strip():
            return [_normalize_stride(stride_values)]

    stride = _normalize_stride(
        str(item.get("stride_category") or item.get("stride") or item.get("category") or item.get("threat_type") or "")
    )
    return [stride]


def _component_to_tf_component(value: str) -> str:
    lowered = value.lower()
    name = _slugify(value)
    mapping: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("aws_s3_bucket", ("s3", "bucket")),
        ("aws_security_group", ("security group", "security_group")),
        ("aws_db_instance", ("database", "db", "rds", "postgres")),
        ("aws_iam_role", ("iam role", "iam", "role")),
        ("aws_iam_policy", ("policy",)),
        ("aws_lambda_function", ("lambda",)),
        ("aws_api_gateway_rest_api", ("api gateway", "api")),
        ("aws_eks_cluster", ("eks", "kubernetes", "k8s")),
        ("aws_ecr_repository", ("ecr",)),
        ("aws_instance", ("ec2", "instance", "bastion")),
        ("aws_cloudfront_distribution", ("cloudfront",)),
        ("aws_route53_zone", ("route53", "route 53", "dns")),
        ("aws_vpc", ("vpc", "subnet")),
        ("aws_wafv2_web_acl", ("waf",)),
    )
    for resource_type, markers in mapping:
        if any(marker in lowered for marker in markers):
            return f"{resource_type}.{name}"
    return f"aws_resource.{name}"


def _extract_component(item: dict[str, Any]) -> str:
    direct = str(item.get("component") or item.get("resource") or item.get("asset") or "").strip()
    if direct:
        return direct

    affected = item.get("affectedComponents")
    if isinstance(affected, list) and affected:
        first = str(affected[0]).strip()
        if first:
            return _component_to_tf_component(first)

    return "unknown.component"


def _extract_description(item: dict[str, Any]) -> str:
    direct = str(
        item.get("description") or item.get("threat_description") or item.get("summary") or item.get("name") or ""
    ).strip()
    if direct:
        return direct

    threat_name = str(item.get("threatName") or "").strip()
    details = item.get("vulnerabilityDetails")
    if isinstance(details, dict):
        how = str(details.get("howItWorks") or "").strip()
        scenario = str(details.get("exploitationScenario") or "").strip()
        combined = " ".join([segment for segment in (threat_name, how, scenario) if segment])
        if combined:
            return combined

    if threat_name:
        return threat_name
    return "Threat imported from ACSE-Eval dataset."


def _extract_references(item: dict[str, Any]) -> list[str]:
    references = _coerce_references(
        item.get("references") if item.get("references") is not None else item.get("evidence")
    )

    frameworks = item.get("frameworks")
    if isinstance(frameworks, dict):
        for framework_key in ("mitreATT&CK", "owaspTop10", "stride"):
            values = frameworks.get(framework_key)
            if isinstance(values, list):
                references.extend([f"{framework_key}: {str(value).strip()}" for value in values if str(value).strip()])
            elif isinstance(values, str) and values.strip():
                references.append(f"{framework_key}: {values.strip()}")

    cwe = str(item.get("cwe") or "").strip()
    if cwe:
        references.append(f"cwe: {cwe}")

    recommendations = item.get("recommendations")
    if isinstance(recommendations, list):
        for recommendation in recommendations:
            if isinstance(recommendation, dict):
                description = str(recommendation.get("description") or "").strip()
                if description:
                    references.append(f"recommendation: {description}")

    # preserve order while removing duplicates
    deduped: list[str] = []
    seen: set[str] = set()
    for reference in references:
        text = reference.strip()
        if not text or text in seen:
            continue
        deduped.append(text)
        seen.add(text)
    return deduped


def normalize_threat_items(item: dict[str, Any], index: int) -> list[dict[str, Any]]:
    component = _extract_component(item)
    description = _extract_description(item)
    threat_id = str(item.get("threat_id") or item.get("id") or item.get("threatID") or f"ACSE-{index + 1:03d}")
    discrepancy_flag = bool(item.get("discrepancy_flag", item.get("discrepancy", False)))
    references = _extract_references(item)
    categories = _extract_stride_categories(item)

    normalized: list[dict[str, Any]] = []
    if len(categories) == 1:
        normalized.append(
            {
                "threat_id": threat_id,
                "stride_category": categories[0],
                "component": component,
                "description": description,
                "discrepancy_flag": discrepancy_flag,
                "references": references,
            }
        )
        return normalized

    for category_index, category in enumerate(categories, start=1):
        normalized.append(
            {
                "threat_id": f"{threat_id}-{category_index}",
                "stride_category": category,
                "component": component,
                "description": description,
                "discrepancy_flag": discrepancy_flag,
                "references": references,
            }
        )
    return normalized


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
                    normalized.extend(normalize_threat_items(item, idx))
            if normalized:
                return normalized

    # Fallback: treat top-level record as one threat if it resembles threat fields.
    if REQUIRED_THREAT_FIELDS.intersection(record.keys()):
        return normalize_threat_items(record, 0)
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
            hydrated_tf = _hydrate_terraform_from_hf_repo(
                repo_id=repo_id,
                infra_path=infra_path,
                timeout_seconds=timeout_seconds,
            )
            if hydrated_tf:
                enriched["terraform"] = hydrated_tf
            else:
                enriched["terraform"] = _synthesize_terraform_from_record(enriched, infra_path=infra_path)

        hydrated.append(enriched)
    return hydrated


def _list_hf_dataset_paths(repo_id: str, base_path: str, timeout_seconds: float) -> list[str]:
    api_url = f"https://huggingface.co/api/datasets/{repo_id}/tree/main/{base_path}?recursive=1"
    response = requests.get(api_url, timeout=timeout_seconds)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        return []
    paths: list[str] = []
    for entry in payload:
        if isinstance(entry, dict) and entry.get("type") == "file":
            path = str(entry.get("path") or "").strip()
            if path:
                paths.append(path)
    return paths


def _hydrate_terraform_from_hf_repo(repo_id: str, infra_path: str, timeout_seconds: float) -> str | None:
    try:
        all_paths = _list_hf_dataset_paths(repo_id=repo_id, base_path=infra_path, timeout_seconds=timeout_seconds)
    except requests.RequestException:
        return None

    tf_paths = [path for path in all_paths if path.endswith(".tf")]
    if not tf_paths:
        return None

    rendered_parts: list[str] = []
    for tf_path in tf_paths:
        url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/{tf_path}"
        try:
            response = requests.get(url, timeout=timeout_seconds)
            response.raise_for_status()
        except requests.RequestException:
            continue
        body = response.text.strip()
        if not body:
            continue
        rendered_parts.append(f"# Source: {tf_path}\n{body}")

    if not rendered_parts:
        return None
    return "\n\n".join(rendered_parts) + "\n"


def _component_to_tf_resource(value: str) -> tuple[str, str]:
    component = _component_to_tf_component(value)
    if "." in component:
        resource_type, resource_name = component.split(".", 1)
        return resource_type, resource_name
    return "aws_resource", _slugify(value)


def _synthesize_terraform_from_record(record: dict[str, Any], infra_path: str) -> str:
    affected_components: list[str] = []
    ground_truth = record.get("ground_truth")
    if isinstance(ground_truth, list):
        for item in ground_truth:
            if isinstance(item, dict):
                components = item.get("affectedComponents")
                if not isinstance(components, list):
                    continue
                for component in components:
                    text = str(component).strip()
                    if text:
                        affected_components.append(text)
    unique_components = sorted(set(affected_components))

    blocks: list[str] = [
        "# ACSE-Eval IaC source path (dataset-relative):",
        f"# {infra_path}",
        "# Terraform source files were not available under this path.",
        "# Synthetic resource stubs generated from affected components:",
        "",
    ]
    for component in unique_components:
        resource_type, resource_name = _component_to_tf_resource(component)
        blocks.append(f'resource "{resource_type}" "{resource_name}" {{')
        blocks.append('  tags = {')
        blocks.append(f'    acse_component = "{component.replace(chr(34), "")}"')
        blocks.append("  }")
        blocks.append("}")
        blocks.append("")

    if not unique_components:
        blocks.append("# No affected components were available to synthesize Terraform stubs.")
    return "\n".join(blocks).rstrip() + "\n"


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
