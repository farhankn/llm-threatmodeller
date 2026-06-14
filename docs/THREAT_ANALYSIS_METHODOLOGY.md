# Threat Analysis Methodology

## Overview
The tool utilizes Large Language Models (LLMs) to perform automated threat modeling based on the **STRIDE** framework. This methodology prioritizes high recall and scientific rigor through structured analysis and grounded inference.

## Analysis Framework: STRIDE
Every resource identified in the infrastructure is evaluated against the six STRIDE categories:
1. **Spoofing**: Identity/authentication threats (e.g., weak IAM policies).
2. **Tampering**: Data/integrity threats (e.g., missing S3 versioning).
3. **Repudiation**: Audit/logging threats (e.g., disabled CloudTrail).
4. **Information Disclosure**: Confidentiality threats (e.g., public storage buckets).
5. **Denial of Service**: Availability threats (e.g., lack of rate limiting).
6. **Elevation of Privilege**: Permission/access threats (e.g., over-privileged roles).

## Threat Discovery Process

### 1. Matrix Reasoning
The system enforces a "Matrix Reasoning" strategy where the LLM is instructed to mentally evaluate every STRIDE category for every identified resource. This breaks the common "one-and-done" bias where an AI might stop after finding the first obvious vulnerability.

### 2. High-Recall Resource Catalog
The LLM's reasoning is guided by a built-in catalog of resource-specific security checks. This catalog provides a "Must-Check" list for common cloud resources (S3, IAM, Security Groups, RDS), ensuring that subtle misconfigurations are not overlooked.

### 3. Contextual Grounding
To minimize hallucinations and maximize precision, the system follows strict grounding rules:
- Every threat must reference an exact Terraform identifier (`resource_type.resource_name`).
- Every threat must cite specific Terraform attributes and their values as evidence.
- A post-generation validation step verifies that all referenced resources and attributes exist in the original IaC files.

## Handling Inconsistencies (Documentation Drift)
When design documents are provided, the tool performs **Discrepancy Detection**. It compares the stated security requirements in the documentation with the actual implementation in code. Gaps are flagged as discrepancies, helping security teams identify drift before deployment.

## Design Decisions
- **Conservative Model Behavior**: The tool is designed to prioritize **Precision** (low noise) by default, but can be configured for **High-Sensitivity** (high recall) through prompt engineering.
- **Deterministic Sampling**: The system uses a temperature of `0.0` to ensure that threat reports are stable and reproducible.
