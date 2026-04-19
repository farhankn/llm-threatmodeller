import json
from pathlib import Path

from threatcli.evaluation.acse_importer import (
    hydrate_records_from_hf_paths,
    import_acse_records,
    load_dataset_records,
)


def test_load_dataset_records_json_and_import(tmp_path: Path) -> None:
    dataset = tmp_path / "acse.json"
    dataset.write_text(
        json.dumps(
            [
                {
                    "id": "sample-1",
                    "terraform": 'resource "aws_s3_bucket" "logs" {}',
                    "design_doc": "Internal logs only.",
                    "ground_truth": [
                        {
                            "threat_id": "GT-1",
                            "stride_category": "Information Disclosure",
                            "component": "aws_s3_bucket.logs",
                            "description": "Public exposure risk.",
                            "discrepancy_flag": True,
                            "references": ["bucket acl"],
                        }
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )
    records = load_dataset_records(dataset)
    result = import_acse_records(records, tmp_path / "fixtures")
    assert result["imported"] == 1
    fixture = tmp_path / "fixtures" / "sample-1"
    assert (fixture / "main.tf").exists()
    assert (fixture / "design.md").exists()
    assert (fixture / "ground_truth.json").exists()


def test_load_dataset_records_jsonl(tmp_path: Path) -> None:
    dataset = tmp_path / "acse.jsonl"
    dataset.write_text(
        '{"id":"row-1","threats":[{"component":"aws_db_instance.app","stride":"Tampering","description":"x"}]}\n',
        encoding="utf-8",
    )
    records = load_dataset_records(dataset)
    assert len(records) == 1
    result = import_acse_records(records, tmp_path / "fixtures")
    assert result["imported"] == 1


def test_hydrate_records_from_hf_paths_enriches_iac_placeholder() -> None:
    records = [
        {
            "id": "row-1",
            "infra_as_code": "row-1/cdk/",
        }
    ]
    hydrated = hydrate_records_from_hf_paths(records)
    assert len(hydrated) == 1
    assert "row-1/cdk/" in hydrated[0]["terraform"]
