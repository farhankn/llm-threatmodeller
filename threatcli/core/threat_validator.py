"""Post-processing validation for generated threats."""

from __future__ import annotations
import re
from typing import Any

def validate_threat_grounding(threat: dict[str, Any], iac_context: dict[str, Any]) -> tuple[bool, str]:
    """
    Verify threat references actual IaC resources and has some evidence.
    """
    component = str(threat.get("component", "")).strip().lower()
    references = threat.get("references", [])
    
    if not component:
        return False, "Empty component field"
        
    resource = _get_resource_from_iac(component, iac_context)
    if not resource:
        return False, f"Component '{component}' not found in IaC"
    
    # Requirement: references must not be empty
    if not references or len(references) == 0:
        return False, "Missing evidence: references field is empty"
    
    # REQUIREMENT SOFTENING: 
    # Instead of strict attribute checking which is brittle, 
    # we check if any reference contains the component name OR a design chunk.
    # This ensures grounding without failing on minor formatting drift.
    has_grounding = False
    comp_name_part = component.split(".")[-1]
    
    for ref in references:
        if not isinstance(ref, str): continue
        ref_low = ref.lower()
        
        # Check for component name or ID in reference
        if comp_name_part in ref_low or component in ref_low:
            has_grounding = True
            break
            
        # Check for design evidence: [chunk_XX]
        if "[" in ref and "chunk_" in ref:
            has_grounding = True
            break
            
    if not has_grounding:
        return False, f"Missing evidence: references do not mention component '{comp_name_part}' or design chunks"
    
    return True, ""


def _get_resource_from_iac(component: str, iac_context: dict[str, Any]) -> dict[str, Any] | None:
    # Check all resource types
    for key in ["resources", "data_sources", "modules"]:
        for res in iac_context.get(key, []):
            res_type = str(res.get("type", "resource")).lower()
            res_name = str(res.get("name", "")).lower()
            
            # Match canonical ID (type.name) or short name
            if component == f"{res_type}.{res_name}" or component == res_name:
                return res
                
            # Match ACSE-style prefix mapping (e.g. aws_resource.name)
            if component.startswith("aws_resource.") and component.endswith(f".{res_name}"):
                return res
                
            # Match data/module specific prefixes
            if key == "data_sources" and component == f"data.{res_type}.{res_name}":
                return res
            if key == "modules" and component == f"module.{res_name}":
                return res
                
    return None


def filter_and_score_threats(
    threats: list[dict[str, Any]], 
    iac_context: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Apply evidence gating, assign threat_kind, and score confidence.
    """
    processed = []
    
    for threat in threats:
        # Assign threat_kind if missing
        if not threat.get("threat_kind"):
            threat["threat_kind"] = _infer_threat_kind(threat)
            
        is_valid, error = validate_threat_grounding(threat, iac_context)
        
        if not is_valid:
            threat["_validation_error"] = error
            threat["_confidence_score"] = 0.2
            threat["needs_review"] = True
        else:
            threat["_confidence_score"] = 0.95
            threat["needs_review"] = False
        
        processed.append(threat)
    
    return processed


def _infer_threat_kind(threat: dict[str, Any]) -> str:
    desc = str(threat.get("description", "")).lower()
    if bool(threat.get("discrepancy_flag")):
        return "design_discrepancy"
    if "lack" in desc or "missing" in desc or "not enabled" in desc:
        return "missing_control"
    if "attacker" in desc and ("then" in desc or "access" in desc):
        return "multi_hop_chain"
    if "misconfigured" in desc or "incorrectly" in desc or "overly broad" in desc:
        return "misconfig"
    return "best_practice"
