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
