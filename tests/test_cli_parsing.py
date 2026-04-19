import pytest

from threatcli.cli import ThreatSchemaError, parse_threats


def test_parse_threats_accepts_raw_json_array() -> None:
    payload = (
        '[{"threat_id":"T-1","stride_category":"Information Disclosure","component":"aws_s3_bucket.a",'
        '"description":"x","discrepancy_flag":false,"references":["r"]}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["threat_id"] == "T-1"


def test_parse_threats_accepts_fenced_json() -> None:
    payload = (
        "```json\n"
        '[{"threat_id":"T-2","stride_category":"Tampering","component":"aws_db_instance.db",'
        '"description":"x","discrepancy_flag":false,"references":["r"]}]\n'
        "```"
    )
    threats = parse_threats(payload)
    assert threats[0]["threat_id"] == "T-2"


def test_parse_threats_accepts_leading_text_then_array() -> None:
    payload = (
        "Here is the result:\n"
        '[{"threat_id":"T-3","stride_category":"Spoofing","component":"aws_iam_user.u",'
        '"description":"x","discrepancy_flag":false,"references":["r"]}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["threat_id"] == "T-3"


def test_parse_threats_still_rejects_non_json() -> None:
    with pytest.raises(ThreatSchemaError):
        parse_threats("not json")


def test_parse_threats_normalizes_alternate_schema() -> None:
    payload = (
        '[{"resource_type":"aws_s3_bucket","resource_name":"public_bucket",'
        '"threat_type":"Information Disclosure","description":"Bucket is public","evidence":"acl public-read"}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["component"] == "aws_s3_bucket.public_bucket"
    assert threats[0]["stride_category"] == "Information Disclosure"
    assert threats[0]["references"] == ["acl public-read"]


def test_parse_threats_normalizes_vertex_variant_schema() -> None:
    payload = (
        '[{"resource":"public_bucket","resource_type":"aws_s3_bucket","threat_type":"Information Disclosure",'
        '"threat_description":"Bucket is public","evidence":"acl public-read"}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["component"] == "aws_s3_bucket.public_bucket"
    assert threats[0]["description"] == "Bucket is public"


def test_parse_threats_normalizes_nested_threat_model_schema() -> None:
    payload = (
        '[{"threat_model":{"threat_id":"STRIDE-T001","resource_type":"aws_db_instance","resource":"app",'
        '"stride_category":"Spoofing","description":"db exposed","evidence":["e1"],"discrepancy":true}}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["threat_id"] == "STRIDE-T001"
    assert threats[0]["component"] == "aws_db_instance.app"
    assert threats[0]["discrepancy_flag"] is True


def test_parse_threats_normalizes_stride_name_without_component() -> None:
    payload = (
        '[{"threat_model":{"name":"Bastion SSH exposure","stride":"Elevation of Privilege",'
        '"description":"SSH open","evidence":["sg rule"],"discrepancy":true}}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["stride_category"] == "Elevation of Privilege"
    assert threats[0]["component"] == "unknown.component"


def test_parse_threats_expands_wrapper_with_threats_list() -> None:
    payload = (
        '[{"threat_model":"STRIDE","threats":[{"name":"open ssh","stride_category":"Tampering",'
        '"description":"ssh open","evidence":"sg allows world"}]}]'
    )
    threats = parse_threats(payload)
    assert len(threats) == 1
    assert threats[0]["stride_category"] == "Tampering"


def test_parse_threats_maps_privilege_escalation_to_stride_category() -> None:
    payload = (
        '[{"threat_model":{"name":"bastion issue","stride":"Privilege Escalation","description":"SSH open",'
        '"evidence":["security group bastion"],"discrepancy":true}}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["stride_category"] == "Elevation of Privilege"


def test_parse_threats_infers_component_from_evidence_text() -> None:
    payload = (
        '[{"threat_model":{"threat_id":"X-1","stride":"Tampering","description":"Open ingress",'
        '"evidence":"aws_security_group bastion ingress 0.0.0.0/0","discrepancy":true}}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["component"] == "aws_security_group.bastion"


def test_parse_threats_uses_parent_resource_when_expanding_grouped_threats() -> None:
    payload = (
        '[{"resource":"aws_s3_bucket.artifacts","threats":[{"stride":"Information Disclosure",'
        '"description":"artifact exposure","evidence":["artifact bucket"],"discrepancy":true}]}]'
    )
    threats = parse_threats(payload)
    assert threats[0]["component"] == "aws_s3_bucket.artifacts"


def test_parse_threats_expands_nested_threat_model_threats_with_parent_resource() -> None:
    payload = (
        '[{"resource":"aws_security_group.bastion","threat_model":{"name":"STRIDE Threat Analysis","threats":['
        '{"stride":"Spoofing","description":"open ssh","evidence":{"infrastructure":"aws_security_group.bastion"},'
        '"discrepancy_flag":true}]}}]'
    )
    threats = parse_threats(payload)
    assert len(threats) == 1
    assert threats[0]["component"] == "aws_security_group.bastion"
