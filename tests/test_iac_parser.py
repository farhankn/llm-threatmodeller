from pathlib import Path

import pytest

from threatcli.parsers.iac_parser import ParseError, discover_tf_files, parse_iac


def _write_tf(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def test_single_resource(tmp_path: Path) -> None:
    tf = tmp_path / "main.tf"
    _write_tf(
        tf,
        """
        resource "aws_s3_bucket" "data_store" {
          acl = "private"
        }
        """,
    )

    resource_map = parse_iac([tf])

    assert len(resource_map["resources"]) == 1
    assert resource_map["resources"][0]["type"] == "aws_s3_bucket"
    assert resource_map["resources"][0]["name"] == "data_store"


def test_multi_resource(tmp_path: Path) -> None:
    tf = tmp_path / "stack.tf"
    _write_tf(
        tf,
        """
        resource "aws_s3_bucket" "data_store" {
          acl = "private"
        }

        resource "aws_db_instance" "app_db" {
          publicly_accessible = false
        }

        resource "aws_security_group" "api_sg" {
          name = "api-sg"
        }
        """,
    )

    resource_map = parse_iac([tf])

    assert len(resource_map["resources"]) == 3


def test_sensitive_redaction(tmp_path: Path) -> None:
    tf = tmp_path / "sensitive.tf"
    _write_tf(
        tf,
        """
        resource "aws_db_instance" "db" {
          password = "hunter2"
          username = "db-admin"
          api_key  = "abc123"
        }
        """,
    )

    resource_map = parse_iac([tf])
    attrs = resource_map["resources"][0]["attributes"]

    assert attrs["password"] == "[REDACTED]"
    assert attrs["api_key"] == "[REDACTED]"
    assert attrs["username"] == "db-admin"


def test_empty_file(tmp_path: Path) -> None:
    tf = tmp_path / "empty.tf"
    tf.write_text("\n", encoding="utf-8")

    resource_map = parse_iac([tf])

    assert resource_map["resources"] == []
    assert resource_map["providers"] == []
    assert resource_map["variables"] == []
    assert resource_map["data_sources"] == []
    assert resource_map["modules"] == []


def test_malformed_file(tmp_path: Path) -> None:
    tf = tmp_path / "broken.tf"
    _write_tf(tf, "resource \"aws_s3_bucket\" \"x\" { acl = \"private\"")

    with pytest.raises(ParseError):
        parse_iac([tf])


def test_directory_discovery(tmp_path: Path) -> None:
    root = tmp_path / "infra"
    nested = root / "modules" / "network"
    nested.mkdir(parents=True)

    _write_tf(root / "main.tf", 'resource "aws_s3_bucket" "a" {}')
    _write_tf(root / "db.tf", 'resource "aws_db_instance" "b" {}')
    _write_tf(nested / "sg.tf", 'resource "aws_security_group" "c" {}')

    resource_map = parse_iac([root])

    assert len(resource_map["resources"]) == 3


def test_extract_provider_variable_data_and_module(tmp_path: Path) -> None:
    tf = tmp_path / "all.tf"
    _write_tf(
        tf,
        """
        provider "aws" {
          region = "us-east-1"
        }

        variable "db_password" {
          type = string
        }

        data "aws_ami" "ubuntu" {
          most_recent = true
          owners = ["099720109477"]
        }

        module "vpc" {
          source = "terraform-aws-modules/vpc/aws"
        }
        """,
    )

    resource_map = parse_iac([tf])

    assert resource_map["providers"][0]["name"] == "aws"
    assert resource_map["providers"][0]["region"] == "us-east-1"
    assert "db_password" in resource_map["variables"]
    assert resource_map["data_sources"][0]["type"] == "aws_ami"
    assert resource_map["modules"][0]["name"] == "vpc"


def test_discover_tf_files_rejects_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(ParseError):
        discover_tf_files([missing])
