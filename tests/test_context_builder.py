import json
import warnings
from pathlib import Path

from threatcli.context_builder import TokenBudgetExceededWarning, build_iac_prompt, build_multisource_prompt
from threatcli.parsers.doc_parser import DocumentChunk


def _extract_summary_from_user_prompt(user_prompt: str) -> dict:
    summary_text = user_prompt.split("### Infrastructure Summary\n", 1)[1].split("\n\n### Task", 1)[0]
    return json.loads(summary_text)


def test_build_iac_prompt_contains_system_and_summary(tmp_path: Path) -> None:
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("SYSTEM PROMPT", encoding="utf-8")

    resource_map = {
        "resources": [{"type": "aws_s3_bucket", "name": "data_store", "attributes": {"acl": "public-read"}}],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    prompt = build_iac_prompt(resource_map, system_prompt_path=prompt_file)

    assert prompt["system"] == "SYSTEM PROMPT"
    assert "### Infrastructure Summary" in prompt["user"]
    assert "aws_s3_bucket" in prompt["user"]
    assert "data_store" in prompt["user"]


def test_token_budget_truncates_modules_before_variables(tmp_path: Path) -> None:
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("SYSTEM PROMPT", encoding="utf-8")

    resource_map = {
        "resources": [
            {
                "type": "aws_s3_bucket",
                "name": "bucket",
                "attributes": {"acl": "private", "description": "x" * 400},
            }
        ],
        "providers": [],
        "variables": ["db_password", "api_token"],
        "data_sources": [],
        "modules": [{"name": "network", "source": "terraform-aws-modules/vpc/aws"}],
    }

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        prompt = build_iac_prompt(resource_map, token_budget=85, system_prompt_path=prompt_file)
    assert any(isinstance(item.message, TokenBudgetExceededWarning) for item in caught)
    summary = _extract_summary_from_user_prompt(prompt["user"])

    assert summary["modules"] == []
    assert summary["variables"] == ["db_password", "api_token"]


def test_token_budget_eventually_truncates_variables(tmp_path: Path) -> None:
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("SYSTEM PROMPT", encoding="utf-8")

    resource_map = {
        "resources": [
            {
                "type": "aws_db_instance",
                "name": "db",
                "attributes": {"notes": "x" * 600},
            }
        ],
        "providers": [],
        "variables": ["db_password", "api_key", "secret_value"],
        "data_sources": [{"type": "aws_ami", "name": "ubuntu", "attributes": {"owners": ["123"]}}],
        "modules": [{"name": "vpc", "source": "terraform-aws-modules/vpc/aws"}],
    }

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        prompt = build_iac_prompt(resource_map, token_budget=30, system_prompt_path=prompt_file)

    assert any(isinstance(item.message, TokenBudgetExceededWarning) for item in caught)
    summary = _extract_summary_from_user_prompt(prompt["user"])

    assert summary["modules"] == []
    assert summary["variables"] == []


def test_build_multisource_prompt_contains_design_context(tmp_path: Path) -> None:
    prompt_file = tmp_path / "multisource.txt"
    prompt_file.write_text("MULTI PROMPT", encoding="utf-8")

    resource_map = {
        "resources": [{"type": "aws_lambda_function", "name": "handler", "attributes": {"runtime": "python3.12"}}],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }
    chunks = [
        DocumentChunk(
            chunk_id="chunk_001",
            heading="Security",
            heading_level=2,
            text="Lambda must not be internet-accessible.",
            section_index=0,
            token_estimate=9,
            has_overlap=False,
        )
    ]

    prompt = build_multisource_prompt(resource_map, chunks, system_prompt_path=prompt_file)

    assert prompt["system"] == "MULTI PROMPT"
    assert "### Design Document Context" in prompt["user"]
    assert "chunk_001" in prompt["user"]
    assert "internet-accessible" in prompt["user"]


def test_build_multisource_prompt_prioritizes_resource_aligned_chunk(tmp_path: Path) -> None:
    prompt_file = tmp_path / "multisource.txt"
    prompt_file.write_text("MULTI PROMPT", encoding="utf-8")

    resource_map = {
        "resources": [
            {
                "type": "aws_resource",
                "name": "aws_directory_service",
                "attributes": {"tags": {"acse_component": "AWS Directory Service"}},
            }
        ],
        "providers": [],
        "variables": [],
        "data_sources": [],
        "modules": [],
    }

    chunks = [
        DocumentChunk(
            chunk_id="chunk_generic",
            heading="General Security",
            heading_level=2,
            text="Generic controls around network and policy hygiene.",
            section_index=0,
            token_estimate=24,
            has_overlap=False,
        ),
        DocumentChunk(
            chunk_id="chunk_component",
            heading="Directory Architecture",
            heading_level=2,
            text="AWS Directory Service authenticates users for desktop sessions.",
            section_index=1,
            token_estimate=24,
            has_overlap=False,
        ),
    ]

    # Force a tiny design-context budget so only one chunk can be selected.
    prompt = build_multisource_prompt(
        resource_map,
        chunks,
        token_budget=80,
        system_prompt_path=prompt_file,
    )

    assert "chunk_component" in prompt["user"]
    assert "chunk_generic" not in prompt["user"]
