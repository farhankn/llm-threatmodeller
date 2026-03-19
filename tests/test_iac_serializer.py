import json

from threatcli.parsers.iac_parser import serialize_resource_map


def test_serialize_resource_map_returns_valid_json() -> None:
    resource_map = {
        "resources": [
            {
                "type": "aws_s3_bucket",
                "name": "data_store",
                "attributes": {"acl": "public-read", "versioning": True},
            }
        ],
        "providers": [{"name": "aws", "region": "us-east-1"}],
        "variables": ["db_password"],
        "data_sources": [],
        "modules": [],
    }

    output = serialize_resource_map(resource_map)
    parsed = json.loads(output)

    assert parsed["resources"][0]["type"] == "aws_s3_bucket"
    assert parsed["resources"][0]["name"] == "data_store"


def test_long_lists_are_truncated() -> None:
    resource_map = {
        "resources": [
            {
                "type": "aws_security_group",
                "name": "api_sg",
                "attributes": {"cidr_blocks": [f"10.0.{i}.0/24" for i in range(15)]},
            }
        ],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    output = json.loads(serialize_resource_map(resource_map))
    cidr_blocks = output["resources"][0]["attributes"]["cidr_blocks"]

    assert len(cidr_blocks) == 11
    assert cidr_blocks[-1] == "...and 5 more"


def test_inline_policy_summarized() -> None:
    resource_map = {
        "resources": [
            {
                "type": "aws_iam_policy",
                "name": "admin",
                "attributes": {
                    "policy": {
                        "Version": "2012-10-17",
                        "Statement": [{"Action": "*", "Effect": "Allow", "Resource": "*"}],
                    }
                },
            }
        ],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    output = json.loads(serialize_resource_map(resource_map))
    policy_summary = output["resources"][0]["attributes"]["policy"]

    assert policy_summary == "[inline policy, 1 statements]"


def test_round_trip_contains_resource_type_and_name() -> None:
    resource_map = {
        "resources": [
            {"type": "aws_s3_bucket", "name": "bucket_a", "attributes": {}},
            {"type": "aws_db_instance", "name": "db_a", "attributes": {}},
            {"type": "aws_lambda_function", "name": "func_a", "attributes": {}},
        ],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    output = serialize_resource_map(resource_map)

    assert "aws_s3_bucket" in output
    assert "bucket_a" in output
    assert "aws_db_instance" in output
    assert "db_a" in output
    assert "aws_lambda_function" in output
    assert "func_a" in output


def test_large_json_gets_compacted() -> None:
    resource_map = {
        "resources": [
            {
                "type": "aws_s3_bucket",
                "name": "bucket",
                "attributes": {
                    "tags": {f"k{i}": f"v{i}" for i in range(20)},
                },
            }
        ],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    output = json.loads(serialize_resource_map(resource_map))
    assert output["resources"][0]["attributes"]["tags"] == "[inline JSON, 20 keys]"
