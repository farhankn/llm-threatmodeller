# Prompt Changelog

## v0.3.0 - 2026-05-09
- **Implemented Ultimate High-Recall Matrix Reasoning:** Overhauled the multi-source prompt to require an internal 6-category STRIDE evaluation for every component.
- **Added Security Catalog Injection:** Injected explicit "Must-Check" security properties for S3, IAM, and Networking into the prompt to guide the LLM's identification of missing controls.
- **Implemented Relationship-Aware Analysis:** Prompt now leverages inferred architectural relationships (e.g., `Lambda -> IAM`) to identify multi-hop attack paths.
- **Strict Grounding Contract:** Enforced exact component naming (`resource_type.resource_name`) to eliminate hallucinations.
- **Few-Shot Examples:** Added example output demonstrating multiple distinct STRIDE threats per component.

## v0.2.0 - 2026-03-22
- Expanded `system_iac_only.txt` with strict STRIDE grounding instructions.
- Added explicit anti-hallucination rules requiring named resource references.
- Added output-schema key contract and allowed STRIDE categories.

## v0.1.0 - 2026-03-22
- Initialized prompt files for IaC-only and multi-source modes.
