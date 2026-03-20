"""Prompt context assembly logic for IaC-only mode."""

from __future__ import annotations

import copy
import math
import warnings
from pathlib import Path
from typing import Any

from threatcli.parsers.iac_parser import serialize_resource_map

DEFAULT_TOKEN_BUDGET = 3000
DEFAULT_IAC_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system_iac_only.txt"


class TokenBudgetExceededWarning(UserWarning):
    """Raised when prompt context must be truncated to fit budget."""


def build_iac_prompt(
    resource_map: dict[str, Any],
    *,
    token_budget: int = DEFAULT_TOKEN_BUDGET,
    system_prompt_path: Path = DEFAULT_IAC_PROMPT_PATH,
) -> dict[str, str]:
    """Build the system/user message pair for IaC-only threat analysis."""
    system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()
    summary = serialize_resource_map(resource_map)

    working_map = copy.deepcopy(resource_map)
    truncation_steps: list[str] = []

    while _estimate_tokens(summary) > token_budget:
        changed = False

        if working_map.get("modules"):
            working_map["modules"] = []
            truncation_steps.append("modules")
            changed = True
        elif working_map.get("variables"):
            working_map["variables"] = []
            truncation_steps.append("variables")
            changed = True
        elif working_map.get("data_sources"):
            working_map["data_sources"] = []
            truncation_steps.append("data_sources")
            changed = True
        else:
            for resource in working_map.get("resources", []):
                if isinstance(resource, dict) and resource.get("attributes"):
                    resource["attributes"] = {}
                    changed = True
            if changed:
                truncation_steps.append("resource_attributes")

        if not changed:
            break

        summary = serialize_resource_map(working_map)

    if truncation_steps:
        warnings.warn(
            TokenBudgetExceededWarning(
                "Token budget exceeded; truncated sections in order: " + ", ".join(truncation_steps)
            ),
            stacklevel=2,
        )

    user_prompt = (
        "### Infrastructure Summary\n"
        f"{summary}\n\n"
        "### Task\n"
        "Identify realistic STRIDE threats grounded in the infrastructure summary. "
        "Return JSON only."
    )

    return {"system": system_prompt, "user": user_prompt}


def _estimate_tokens(text: str) -> int:
    """Approximate token count from character length."""
    return math.ceil(len(text) / 4)
