"""Rule-based mapping of threat patterns to security frameworks (MITRE ATT&CK, CWE, OWASP)."""

from __future__ import annotations
import re
from typing import Any

# Pattern-to-Framework mapping rules
FRAMEWORK_RULES = [
    {
        "id": "S3_PUBLIC",
        "keywords": ["s3", "public", "bucket", "exposure"],
        "mappings": {
            "mitreATT&CK": ["T1530 - Data from Cloud Storage Object"],
            "cwe": ["CWE-284 - Improper Access Control"],
            "owaspTop10": ["A01:2021 - Broken Access Control"]
        }
    },
    {
        "id": "IAM_WILDCARD",
        "keywords": ["iam", "wildcard", "permissions", "*"],
        "mappings": {
            "mitreATT&CK": ["T1078 - Valid Accounts"],
            "cwe": ["CWE-269 - Improper Privilege Management"],
            "owaspTop10": ["A01:2021 - Broken Access Control"]
        }
    },
    {
        "id": "UNENCRYPTED_DATA",
        "keywords": ["encryption", "unencrypted", "plaintext", "at rest"],
        "mappings": {
            "mitreATT&CK": ["T1530 - Data from Cloud Storage Object"],
            "cwe": ["CWE-311 - Missing Encryption of Sensitive Data"],
            "owaspTop10": ["A02:2021 - Cryptographic Failures"]
        }
    },
    {
        "id": "NETWORK_EXPOSURE",
        "keywords": ["security group", "0.0.0.0", "ingress", "port"],
        "mappings": {
            "mitreATT&CK": ["T1190 - Exploit Public-Facing Application"],
            "cwe": ["CWE-284 - Improper Access Control"],
            "owaspTop10": ["A05:2021 - Security Misconfiguration"]
        }
    }
]

def map_threat_to_frameworks(threat: dict[str, Any]) -> dict[str, Any]:
    """Enhance threat with best-effort framework mappings based on description."""
    references = threat.get("references", [])
    if not isinstance(references, list):
        references = []
        
    desc = str(threat.get("description", "")).lower()
    comp = str(threat.get("component", "")).lower()
    text = f"{comp} {desc}"
    
    # Only add if MITRE/CWE/OWASP not already present
    has_mitre = any("mitre" in str(r).lower() for r in references)
    has_cwe = any("cwe" in str(r).lower() for r in references)
    has_owasp = any("owasp" in str(r).lower() for r in references)
    
    new_refs = []
    for rule in FRAMEWORK_RULES:
        if all(kw.lower() in text for kw in rule["keywords"]):
            if not has_mitre: new_refs.extend([f"mitreATT&CK: {m}" for m in rule["mappings"]["mitreATT&CK"]])
            if not has_cwe: new_refs.extend([f"cwe: {m}" for m in rule["mappings"]["cwe"]])
            if not has_owasp: new_refs.extend([f"owaspTop10: {m}" for m in rule["mappings"]["owaspTop10"]])
            break # Match first rule
            
    threat["references"] = references + new_refs
    return threat
