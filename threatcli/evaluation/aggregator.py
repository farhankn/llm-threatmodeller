"""Logic for aggregating and merging threat models from multiple LLM providers."""

from __future__ import annotations

from typing import Any


def merge_threat_models(
    outputs: list[list[dict[str, Any]]], 
    strategy: str = "union"
) -> list[dict[str, Any]]:
    """
    Merge multiple threat model lists into one.
    
    Strategies:
    - union: Keep all unique threats from all models (Maximize Recall).
    - consensus: Keep only threats identified by at least 2 models (Maximize Precision).
    """
    if not outputs:
        return []
    if len(outputs) == 1:
        return outputs[0]

    all_threats = []
    for output_list in outputs:
        all_threats.extend(output_list)

    if strategy == "union":
        return _deduplicate_by_identity(all_threats)
    
    if strategy == "consensus":
        return _find_consensus(outputs)

    return all_threats


def _deduplicate_by_identity(threats: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {}
    for threat in threats:
        # Identity is (component, category)
        key = (
            str(threat.get("component", "")).lower(),
            str(threat.get("stride_category", "")).lower()
        )
        if key not in seen:
            seen[key] = threat
        else:
            # Prefer the one with a discrepancy flag or longer description
            existing = seen[key]
            if bool(threat.get("discrepancy_flag")) and not bool(existing.get("discrepancy_flag")):
                seen[key] = threat
            elif len(str(threat.get("description", ""))) > len(str(existing.get("description", ""))):
                seen[key] = threat
    return list(seen.values())


def _find_consensus(outputs: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    from collections import Counter
    
    # Count occurrences of (component, category)
    counts = Counter()
    identity_map = {}
    
    for output_list in outputs:
        for threat in output_list:
            key = (
                str(threat.get("component", "")).lower(),
                str(threat.get("stride_category", "")).lower()
            )
            counts[key] += 1
            # Store the 'best' version of the threat for each key
            if key not in identity_map or bool(threat.get("discrepancy_flag")):
                identity_map[key] = threat

    # Keep only those with at least 2 votes
    consensus_keys = [key for key, count in counts.items() if count >= 2]
    return [identity_map[key] for key in consensus_keys]
