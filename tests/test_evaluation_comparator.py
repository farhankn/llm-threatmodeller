import json
from pathlib import Path

from threatcli.evaluation.comparator import build_known_components, compare, load_ground_truth, load_llm_output


def test_load_ground_truth_from_fixture() -> None:
    data = load_ground_truth("tests/fixtures/tri_01/ground_truth.json")
    assert isinstance(data, list)
    assert data[0]["component"] == "aws_s3_bucket.public_bucket"


def test_load_llm_output_from_string() -> None:
    output = '[{"threat_id":"X","stride_category":"Information Disclosure","component":"aws_s3_bucket.public_bucket","description":"x","discrepancy_flag":false,"references":[]}]'
    data = load_llm_output(output)
    assert len(data) == 1
    assert data[0]["threat_id"] == "X"


def test_build_known_components() -> None:
    resource_map = {
        "resources": [{"type": "aws_s3_bucket", "name": "public_bucket", "attributes": {}}],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }
    known = build_known_components(resource_map)
    assert "aws_s3_bucket" in known
    assert "public_bucket" in known
    assert "aws_s3_bucket.public_bucket" in known


def test_compare_computes_metrics() -> None:
    gt = [
        {
            "threat_id": "T-1",
            "stride_category": "Information Disclosure",
            "component": "aws_s3_bucket.public_bucket",
            "description": "x",
            "discrepancy_flag": True,
            "references": [],
        }
    ]
    out = [
        {
            "threat_id": "O-1",
            "stride_category": "Information Disclosure",
            "component": "aws_s3_bucket.public_bucket",
            "description": "x",
            "discrepancy_flag": True,
            "references": [],
        },
        {
            "threat_id": "O-2",
            "stride_category": "Tampering",
            "component": "aws_unknown.x",
            "description": "x",
            "discrepancy_flag": False,
            "references": [],
        },
    ]
    resource_map = {
        "resources": [{"type": "aws_s3_bucket", "name": "public_bucket", "attributes": {}}],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }
    result = compare(out, gt, resource_map)
    assert result["tp"] == 1
    assert result["fp"] == 1
    assert result["fn"] == 0
    assert result["precision"] == 0.5
    assert result["recall"] == 1.0
    assert result["jaccard_index"] == 0.5
    assert result["ddr"] == 1.0
    assert result["hallucination_rate"] == 0.5
    assert result["stride_tfc_tp"] == 1
    assert result["stride_tfc_total"] == 1
    assert result["stride_tfc_recall"] == 1.0
    assert result["mitre_tfc_tp"] == 0
    assert result["mitre_tfc_total"] == 0
    assert result["mitre_tfc_recall"] == 0.0


def test_load_llm_output_from_file(tmp_path: Path) -> None:
    p = tmp_path / "out.json"
    p.write_text(
        json.dumps(
            [
                {
                    "threat_id": "T-1",
                    "stride_category": "Spoofing",
                    "component": "aws_iam_role.app",
                    "description": "x",
                    "discrepancy_flag": False,
                    "references": [],
                }
            ]
        ),
        encoding="utf-8",
    )
    data = load_llm_output(str(p))
    assert data[0]["component"] == "aws_iam_role.app"


def test_compare_fuzzy_component_and_stride_alias_matching() -> None:
    gt = [
        {
            "threat_id": "T-1",
            "stride_category": "Elevation of Privilege",
            "component": "aws_security_group.bastion",
            "description": "x",
            "discrepancy_flag": True,
            "references": [],
        }
    ]
    out = [
        {
            "threat_id": "O-1",
            "stride_category": "Privilege Escalation",
            "component": "aws_instance.bastion",
            "description": "x",
            "discrepancy_flag": True,
            "references": [],
        }
    ]
    resource_map = {
        "resources": [
            {"type": "aws_security_group", "name": "bastion", "attributes": {}},
            {"type": "aws_instance", "name": "bastion", "attributes": {}},
        ],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }
    result = compare(out, gt, resource_map)
    assert result["tp"] == 1
    assert result["fp"] == 0
    assert result["fn"] == 0


def test_compare_tracks_mitre_framework_coverage_from_references() -> None:
    gt = [
        {
            "threat_id": "GT-1",
            "stride_category": "Information Disclosure",
            "component": "aws_s3_bucket.logs",
            "description": "x",
            "discrepancy_flag": False,
            "references": ["mitreATT&CK: T1530 - Data from Cloud Storage Object"],
            "frameworks": {"mitreATT&CK": ["T1530 - Data from Cloud Storage Object"]},
        }
    ]
    out = [
        {
            "threat_id": "OUT-1",
            "stride_category": "Information Disclosure",
            "component": "aws_s3_bucket.logs",
            "description": "x",
            "discrepancy_flag": False,
            "references": ["mitreATT&CK: T1530"],
        }
    ]
    resource_map = {
        "resources": [{"type": "aws_s3_bucket", "name": "logs", "attributes": {}}],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    result = compare(out, gt, resource_map)
    assert result["mitre_tfc_tp"] == 1
    assert result["mitre_tfc_total"] == 1
    assert result["mitre_tfc_recall"] == 1.0
