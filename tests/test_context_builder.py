import json
import warnings
from pathlib import Path

from threatcli.context_builder import TokenBudgetExceededWarning, build_iac_prompt


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
        prompt = build_iac_prompt(resource_map, token_budget=80, system_prompt_path=prompt_file)

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
