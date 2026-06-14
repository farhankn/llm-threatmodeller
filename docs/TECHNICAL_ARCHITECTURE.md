# Technical Architecture: Automated Threat Modeling CLI

## Overview
The Automated Threat Modeling CLI is a tool designed to analyze cloud infrastructure (Terraform) and design documentation (Markdown) to identify security threats using Large Language Models (LLMs). It follows a single-pass analysis pipeline where context from multiple sources is fused and presented to an LLM for structured threat generation.

## Components

### 1. IaC Parser (`threatcli/parsers/iac_parser.py`)
- Responsible for parsing Terraform HCL files using `python-hcl2`.
- Extracts a structured `ResourceMap` containing resources, variables, modules, and providers.
- Performs sensitive value redaction to prevent secret leakage in prompts.
- **Relationship Inference**: Automatically identifies connections between resources (e.g., IAM roles attached to Lambda functions) to provide architectural context.

### 2. Document Parser (`threatcli/parsers/doc_parser.py`)
- Reads and chunks Markdown design documents.
- Implements heading-aware segmentation and paragraph-level chunking with overlap.
- Metadata is preserved for each chunk (heading, position, token estimate).

### 3. Context Builder (`threatcli/threatcli/context_builder.py`)
- Fuses context from the IaC summary and document chunks into a single LLM prompt.
- **Relevance Scoring**: Implements a weighted heuristic to select the most important document chunks based on keyword overlap with IaC resources, security term density, and heading relevance.
- Manages token budgets to ensure critical information is prioritized.

### 4. LLM Client (`threatcli/llm_client.py`)
- Pluggable architecture supporting multiple providers (OpenAI, Gemini/Vertex, Ollama).
- Handles transport-level concerns like retries and rate limiting.

### 5. Threat Validator (`threatcli/core/threat_validator.py`)
- Post-processes LLM-generated threats.
- Verifies that every reported threat is grounded in actual IaC resources and attributes.
- Filters out potential hallucinations.

### 6. Renderer (`threatcli/renderer.py`)
- Formats threats into multiple output types:
    - **Terminal**: Rich-formatted tables grouped by STRIDE.
    - **JSON**: Structured data for CI/CD integration.
    - **PDF**: Professional byte-stream generated reports.

## Pipeline Flow
1. **Input**: User provides IaC files and optional design docs.
2. **Parsing**: IaC and docs are parsed into intermediate representations.
3. **Fusion**: Context builder assembles the final prompt.
4. **Inference**: LLM generates threats in JSON format.
5. **Validation**: Validator checks grounding and scores confidence.
6. **Output**: Renderer generates the final report in the requested format.
