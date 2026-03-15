# Automated Threat Modeling CLI using LLMs
## System Design Document

> **Author:** Mohammed Farhan · **Version:** 1.0 · **Date:** March 2026 · **Status:** Draft

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Module Design](#3-module-design)
4. [Threat Output Schema](#4-threat-output-schema)
5. [Phase 1 — Tasks](#5-phase-1--tasks)
6. [Phase 1 — Task Summary](#6-phase-1--task-summary)
7. [Technical Risks and Mitigations](#7-technical-risks-and-mitigations)

---

## 1. Introduction

### 1.1 Purpose

This document describes the system architecture and design of the **Automated Threat Modeling CLI** — a command-line tool that leverages Large Language Models (LLMs) to generate STRIDE-based threat models from Infrastructure-as-Code (IaC) files and Design Documents. It serves as the primary reference for development, testing, and evaluation throughout the project lifecycle.

### 1.2 Scope

The tool accepts Terraform (`.tf`) files and Markdown/text Design Documents as input. It processes these through an LLM backend to produce structured STRIDE threat reports. The system is designed to run as a standalone CLI and to be embeddable within CI/CD pipelines.

### 1.3 Definitions

| Term | Definition |
|------|-----------|
| **CLI** | Command-Line Interface |
| **IaC** | Infrastructure-as-Code — declarative config files (e.g. Terraform/HCL) defining cloud infrastructure |
| **LLM** | Large Language Model (e.g. GPT-4, Claude) used for NL understanding and generation |
| **STRIDE** | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
| **HCL** | HashiCorp Configuration Language — the syntax used by Terraform |
| **Context Fusion** | Combining IaC summaries and design narrative into a single structured LLM prompt |
| **Chunking** | Splitting a large document into smaller segments to stay within LLM token limits |
| **Hallucination** | An LLM output referencing components not present in the provided input |

---

## 2. System Overview

### 2.1 High-Level Architecture

The system is composed of **five loosely coupled modules** forming a linear processing pipeline. Input artefacts are ingested, parsed, and fused into a structured prompt, which is sent to an LLM backend. The response is then parsed and rendered as a formatted threat report.

```mermaid
graph LR
    subgraph INPUT["Input Layer"]
        A["Terraform Files\n(.tf / HCL)"]
        B["Design Documents\n(.md / .txt)"]
    end

    subgraph PARSE["Parse Layer"]
        C["IaC Parser\npython-hcl2"]
        D["Document Parser\nChunking Logic"]
    end

    subgraph FUSE["Fusion Layer"]
        E["Context Builder\nPrompt Assembly"]
        F["Prompt Templates\nprompts/*.txt"]
    end

    subgraph INFER["Inference Layer"]
        G["LLM Client\nOpenAI / Anthropic / Ollama"]
    end

    subgraph RENDER["Output Layer"]
        H["Report Renderer\ntext / JSON / PDF"]
    end

    A --> C
    B --> D
    C --> E
    D --> E
    F --> E
    E --> G
    G --> H
```

### 2.2 Data Flow

```mermaid
sequenceDiagram
    actor User
    participant CLI as CLI Entry Point
    participant IaC as IaC Parser
    participant Doc as Document Parser
    participant CB as Context Builder
    participant LLM as LLM Client
    participant RR as Report Renderer

    User->>CLI: threatcli analyze --iac infra.tf --doc design.md
    CLI->>CLI: Validate inputs and flags
    CLI->>IaC: parse(tf_files)
    IaC-->>CLI: ResourceMap (JSON)
    CLI->>Doc: parse(design_doc)
    Doc-->>CLI: Ordered chunks[]
    CLI->>CB: build_prompt(resource_map, chunks)
    CB-->>CLI: system + user prompt dict
    CLI->>LLM: generate(prompt, temperature=0.5)
    LLM-->>CLI: Raw JSON threat list
    CLI->>RR: render(threats, format="text")
    RR-->>User: Formatted threat model report
```

### 2.3 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.11+ | Strong ecosystem for CLI tooling, NLP, and LLM API clients |
| **CLI Framework** | Click / Typer | Declarative argument parsing, auto-generated help, testability |
| **IaC Parsing** | `python-hcl2` | Native HCL2 parser; outputs Python dicts |
| **Document Parsing** | `markdown-it-py` + stdlib | Lightweight Markdown parsing, no heavy dependencies |
| **LLM Backend** | OpenAI API / Anthropic API / Ollama | Pluggable; provider selected via config flag |
| **Output Rendering** | Rich (terminal) + json + ReportLab (PDF) | Progressive enhancement layered on top of plain JSON |
| **Testing** | `pytest` + `pytest-cov` | Standard Python testing; coverage reporting for CI |
| **Version Control** | Git + GitHub Actions | CI/CD hooks; automated test runs on every push |

---

## 3. Module Design

### 3.1 CLI Entry Point

The entry point (`cli.py`) is responsible for the user-facing interface and pipeline orchestration.

#### Commands

| Command | Description |
|---------|-------------|
| `analyze` | Primary command — accepts IaC paths and optional design doc, runs full pipeline |
| `validate` | Checks that provided files are parseable before running analysis |
| `version` | Prints tool version and active LLM provider configuration |

#### Key Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--iac / -i` | Path (multiple) | — | One or more Terraform file or directory paths |
| `--doc / -d` | Path (optional) | — | Design document path (`.md` or `.txt`) |
| `--format / -f` | `text\|json\|pdf` | `text` | Output format |
| `--output / -o` | Path (optional) | stdout | Write output to file |
| `--temperature` | Float 0.0–1.0 | `0.5` | LLM temperature setting |
| `--model` | String | provider default | Override LLM model name |
| `--provider` | `openai\|anthropic\|ollama` | `openai` | Select LLM backend provider |

---

### 3.2 IaC Parser

The IaC Parser reads `.tf` files and produces a normalised **ResourceMap** using `python-hcl2`.

```mermaid
flowchart TD
    A["Input: .tf File Paths"] --> B{Directory\nor files?}
    B -->|Directory| C["glob **/*.tf\nrecursive=True"]
    B -->|Files| D["Direct file list"]
    C --> E["Read and Parse HCL\nvia python-hcl2"]
    D --> E
    E --> F{Parse\nsuccessful?}
    F -->|No| G["Raise ParseError\n+ human-readable message"]
    F -->|Yes| H["Extract Blocks:\nresource / provider\nvariable / data / module"]
    H --> I["Redact sensitive values\npatterns: password, secret, key, token"]
    I --> J["Return ResourceMap dict"]
```

#### ResourceMap Schema

```json
{
  "resources":    [{ "type": "aws_s3_bucket", "name": "data_store", "attributes": { "acl": "public-read" } }],
  "providers":    [{ "name": "aws", "region": "eu-west-1" }],
  "variables":    ["db_password", "api_key"],
  "data_sources": [{ "type": "aws_ami", "name": "ubuntu" }],
  "modules":      [{ "name": "vpc", "source": "terraform-aws-modules/vpc/aws" }]
}
```

> **Security note:** Sensitive attribute values matching patterns (`password`, `secret`, `key`, `token`) are replaced with `[REDACTED]` before the summary is passed downstream.

---

### 3.3 Document Parser

The Document Parser segments the design document into chunks that fit within the LLM token budget.

```mermaid
flowchart LR
    A["Raw Document\n.md / .txt"] --> B["Split at\nHeading boundaries"]
    B --> C{Section size\n> 1,500 tokens?}
    C -->|No| D["Keep section\nas single chunk"]
    C -->|Yes| E["Split at\nparagraph boundaries"]
    E --> F["Add 100-token\noverlap between chunks"]
    D --> G["Prepend section\nmetadata header"]
    F --> G
    G --> H["Output: List of\nheading + text tuples"]
```

| Parameter | Value | Configurable |
|-----------|-------|-------------|
| Max chunk size | 1,500 tokens | Yes |
| Overlap between chunks | 100 tokens | Yes |
| Metadata prepended | Heading text + level | No |

---

### 3.4 Context Builder

The Context Builder is the **most architecturally significant module** — it implements the Context Fusion strategy central to Research Question 1.

```mermaid
graph TD
    A["Prompt Template\nprompts/system_iac_only.txt\nor system_multisource.txt"]
    B["IaC Resource Summary\nserialised JSON"]
    C["Design Document Chunks\nwhen --doc is provided"]
    D["Context Builder\nbuild_prompt()"]
    E["Assembled Prompt Dict\nsystem message + user message"]
    F["TokenBudgetExceededWarning\nif > 3,000 tokens"]

    A --> D
    B --> D
    C --> D
    D --> E
    D -.->|truncate variables and modules first| F
```

#### Prompt Structure

```
+----------------------------------------------------------+
|  SECTION 1: System Instruction                           |
|  "You are a senior cloud security architect..."          |
+----------------------------------------------------------+
|  SECTION 2: Context Block                                |
|  ### Infrastructure Summary (IaC)                        |
|  { ...serialised ResourceMap JSON... }                   |
|                                                          |
|  ### Design Document (when --doc provided)               |
|  [Chunk 1: Authentication Flow]                          |
|  This service handles OAuth2 tokens...                   |
+----------------------------------------------------------+
|  SECTION 3: Task Instruction                             |
|  "Return your analysis as a JSON array.                  |
|   Each object must contain: threat_id,                   |
|   stride_category, component, description..."            |
+----------------------------------------------------------+
```

---

### 3.5 LLM Client

The LLM Client abstracts over multiple LLM providers via a common interface.

```mermaid
classDiagram
    class LLMClient {
        <<abstract>>
        +generate(prompt: dict, temperature: float) str
    }

    class OpenAIClient {
        -api_key: str
        -model: str
        +generate(prompt, temperature) str
        -_retry_with_backoff(fn) str
    }

    class AnthropicClient {
        -api_key: str
        -model: str
        +generate(prompt, temperature) str
        -_retry_with_backoff(fn) str
    }

    class OllamaClient {
        -base_url: str
        -model: str
        +generate(prompt, temperature) str
    }

    LLMClient <|-- OpenAIClient
    LLMClient <|-- AnthropicClient
    LLMClient <|-- OllamaClient
```

#### Retry Logic

```
Attempt 1 --> [wait 1s] --> Attempt 2 --> [wait 2s] --> Attempt 3 --> FAIL
              429 / 5xx                   429 / 5xx                    |
                                                               Raise LLMError
```

- **Max retries:** 3
- **Backoff factor:** 2x (1s then 2s then 4s)
- **Hard timeout:** 60 seconds per request
- **Triggers:** HTTP 429 (rate limit) and HTTP 5xx (server error)

---

### 3.6 Report Renderer

| Format | Output | Description |
|--------|--------|-------------|
| `text` (default) | Terminal | Colour-coded output via **Rich**. Groups threats by STRIDE category. Discrepancies highlighted in amber. |
| `json` | File / stdout | Pretty-printed JSON array of threat objects. Pipeable to other tools. |
| `pdf` | File | Structured PDF via ReportLab — cover summary, threat table, discrepancy section. |

---

## 4. Threat Output Schema

All generated threats conform to this JSON schema, included in the LLM prompt as a structured output instruction.

```json
{
  "threat_id":          "T-001",
  "stride_category":    "Information Disclosure",
  "component":          "aws_s3_bucket.data_store",
  "description":        "S3 bucket has public-read ACL, exposing all objects to unauthenticated access.",
  "discrepancy_flag":   true,
  "discrepancy_detail": "Design doc states 'internal storage only' but ACL is set to public-read.",
  "severity":           "High",
  "references":         ["aws_s3_bucket.data_store.acl = \"public-read\""]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `threat_id` | String | Yes | Auto-generated identifier (e.g. `T-001`) |
| `stride_category` | Enum | Yes | One of the six STRIDE categories |
| `component` | String | Yes | Terraform resource or design component the threat applies to |
| `description` | String | Yes | Human-readable description of the threat |
| `discrepancy_flag` | Boolean | Yes | `true` if threat arises from design-vs-IaC conflict |
| `discrepancy_detail` | String | No | Description of the specific conflict (when flag is `true`) |
| `severity` | Enum | No | `High`, `Medium`, or `Low` — populated by post-processing heuristic |
| `references` | String[] | Yes | Source lines from Terraform/doc anchoring the threat (anti-hallucination) |

---

## 5. Phase 1 — Tasks

> **Timeline:** Weeks 3–4 (March) · **Goal:** Implement the HCL parser, design initial STRIDE prompt templates, and build the graduated test suite for IaC-only inputs.

```mermaid
gantt
    title Phase 1 Task Schedule (2 Weeks)
    dateFormat  DD
    axisFormat  Day %d

    section Foundation
    P1-T01 Project Skeleton           :t01, 01, 2d

    section IaC Parser
    P1-T02 Core Resource Extraction   :t02, after t01, 3d
    P1-T03 JSON Summary Serialiser    :t03, after t02, 2d

    section Prompts and Context
    P1-T04 STRIDE Prompt Templates    :t04, after t03, 2d
    P1-T05 Context Builder            :t05, after t03, 2d

    section LLM and Testing
    P1-T06 LLM Client                 :t06, after t05, 3d
    P1-T07 Graduated Test Suite       :t07, after t06, 3d
    P1-T08 CLI Wiring and Smoke Test  :t08, after t07, 2d
```

---

### Task P1-T01 — Project Skeleton and Environment Setup

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T01 |
| **Estimate** | 2–3 hours |
| **Status** | To Do |
| **Depends On** | — |

**Description:** Initialise the Python project repository with the correct structure, dependency management, and CI hooks before any feature code is written. This task establishes the foundation that all subsequent Phase 1 tasks build upon.

**Acceptance Criteria:**
- [ ] Git repository exists with an initial commit containing the full project skeleton
- [ ] `pyproject.toml` declares all direct dependencies (`click`/`typer`, `python-hcl2`, `openai`, `anthropic`, `rich`, `pytest`, `pytest-cov`)
- [ ] Virtual environment can be created and all dependencies installed with `pip install -e ".[dev]"`
- [ ] `.github/workflows/ci.yml` runs `pytest` on every push and fails if any test fails
- [ ] Directory structure matches the layout below
- [ ] `README.md` contains: project description, installation steps, placeholder usage example

**Directory Structure:**

```
threat-model-cli/
├── threatcli/
│   ├── __init__.py
│   ├── cli.py                  # Entry point
│   ├── parsers/
│   │   ├── iac_parser.py
│   │   └── doc_parser.py
│   ├── context_builder.py
│   ├── llm_client.py
│   └── renderer.py
├── prompts/
│   ├── CHANGELOG.md
│   ├── system_iac_only.txt
│   └── system_multisource.txt
├── tests/
│   ├── fixtures/
│   └── test_iac_parser.py
├── pyproject.toml
└── README.md
```

---

### Task P1-T02 — HCL Parser: Core Resource Extraction

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T02 |
| **Estimate** | 4–6 hours |
| **Status** | To Do |
| **Depends On** | P1-T01 |

**Description:** Implement the IaC Parser module (`iac_parser.py`) that reads one or more Terraform `.tf` files and produces a normalised ResourceMap. This is foundational to all downstream threat generation.

**Acceptance Criteria:**
- [ ] Parser accepts a list of file paths and returns a Python dict conforming to the ResourceMap schema
- [ ] Correctly extracts: `resource`, `provider`, `variable`, `data`, and `module` blocks
- [ ] Sensitive attribute names (`password`, `secret`, `key`, `token`) are replaced with `[REDACTED]`
- [ ] Malformed or empty `.tf` files raise a `ParseError` with a human-readable message
- [ ] Recursively discovers all `.tf` files within a directory path via `glob('**/*.tf', recursive=True)`
- [ ] Unit tests cover all cases in the test matrix below

**Unit Test Matrix:**

| Test Case | Input | Expected Result |
|-----------|-------|----------------|
| `test_single_resource` | `.tf` with one `aws_s3_bucket` | ResourceMap with 1 resource entry |
| `test_multi_resource` | `.tf` with S3 + RDS + security group | ResourceMap with 3 resource entries |
| `test_sensitive_redaction` | `.tf` with `password = "hunter2"` | Value replaced with `[REDACTED]` |
| `test_empty_file` | Empty `.tf` | Empty ResourceMap (no error raised) |
| `test_malformed_file` | Invalid HCL syntax | `ParseError` raised |
| `test_directory_discovery` | Directory with 3 `.tf` files | All 3 files parsed and merged |

---

### Task P1-T03 — HCL Parser: JSON Summary Serialiser

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T03 |
| **Estimate** | 2–3 hours |
| **Status** | To Do |
| **Depends On** | P1-T02 |

**Description:** Implement a serialiser that converts the ResourceMap into a compact, human-readable JSON summary string suitable for LLM prompt inclusion. Must balance completeness (enough detail for threat identification) with brevity (minimise token consumption).

**Acceptance Criteria:**
- [ ] `serialize_resource_map(resource_map: dict) -> str` returns a valid JSON string
- [ ] Output for a typical 10-resource Terraform file does not exceed **2,000 tokens** (estimated by character-count heuristic)
- [ ] Keys use `snake_case`; nested objects are indented; long lists (>10 items) are truncated with `"...and N more"`
- [ ] Large inline policy JSON is summarised as `"[inline policy, N statements]"` rather than expanded in full
- [ ] Round-trip test: serialised summary contains the resource type and name for every resource in the original map

**Serialisation Rules:**

```
Resource attribute  -->  Include if: boolean flag OR short string (< 100 chars)
Large JSON value    -->  Summarise as "[inline JSON, N keys]"
Long list           -->  Truncate at 10 items, append "...and N more"
Sensitive value     -->  Already redacted by parser; include as "[REDACTED]"
```

---

### Task P1-T04 — STRIDE Prompt Templates (IaC-Only)

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T04 |
| **Estimate** | 3–4 hours |
| **Status** | To Do |
| **Depends On** | P1-T03 |

**Description:** Design, write, and manually validate the first set of STRIDE-aligned prompt templates for IaC-only analysis mode. Prompt engineering is a **first-class deliverable** — these versioned templates directly determine the quality of generated threat models.

**Acceptance Criteria:**
- [ ] `prompts/system_iac_only.txt` exists as a versioned prompt file
- [ ] Prompt instructs LLM to: act as a security architect, analyse IaC summary, identify threats per STRIDE category, return output in the defined JSON schema
- [ ] Prompt explicitly instructs LLM to ground each threat in a **named resource** from the input (anti-hallucination measure)
- [ ] Prompt manually tested against at least 2 LLM providers (e.g. GPT-4o and Claude Sonnet) with a trivial input (single public S3 bucket)
- [ ] Negative test performed: Terraform with no obvious misconfigs must not produce fabricated threats
- [ ] `prompts/CHANGELOG.md` records the version, date, and rationale for this prompt iteration

**Prompt Template Anatomy:**

```
+----------------------------------------------------------------+
| ROLE DEFINITION                                                |
| "You are a senior cloud security architect specialising in     |
|  threat modeling for cloud-native infrastructure..."           |
+----------------------------------------------------------------+
| TASK DESCRIPTION                                               |
| "Analyse the following Terraform infrastructure summary and    |
|  identify security threats for each STRIDE category..."        |
+----------------------------------------------------------------+
| GROUNDING INSTRUCTION                                          |
| "Every threat MUST reference at least one resource name from   |
|  the infrastructure summary. Do not invent components."        |
+----------------------------------------------------------------+
| COMPLETENESS INSTRUCTION                                       |
| "If no threat exists for a STRIDE category, return an empty    |
|  array for that category rather than inventing threats."       |
+----------------------------------------------------------------+
| OUTPUT SCHEMA                                                  |
| "Return ONLY a JSON array. Each object must contain:           |
|  threat_id, stride_category, component, description,           |
|  discrepancy_flag, references"                                 |
+----------------------------------------------------------------+
```

---

### Task P1-T05 — Context Builder (IaC-Only Mode)

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T05 |
| **Estimate** | 3–4 hours |
| **Status** | To Do |
| **Depends On** | P1-T03, P1-T04 |

**Description:** Implement the Context Builder module (`context_builder.py`) for the IaC-only path. Loads the prompt template, injects the serialised IaC summary, and returns the fully assembled prompt dict ready for the LLM Client.

**Acceptance Criteria:**
- [ ] `build_iac_prompt(resource_map: dict) -> dict` returns `{"system": "...", "user": "..."}` matching the OpenAI messages format
- [ ] User message contains the serialised IaC summary injected into a clearly marked `### Infrastructure Summary` section
- [ ] If the summary exceeds **3,000 tokens** (configurable), raises `TokenBudgetExceededWarning` and truncates in order: variable blocks first, then module blocks
- [ ] Unit-tested with a mocked resource map — output must contain expected resource type and name strings

**Token Budget Truncation Order:**

```mermaid
flowchart LR
    A["Serialised ResourceMap"] --> B{Size > 3,000 tokens?}
    B -->|No| D["Inject into prompt as-is"]
    B -->|Yes| C["Truncate in order:\n1. module blocks\n2. variable blocks\n3. data sources\n4. resource attributes"]
    C --> E["Raise TokenBudgetExceededWarning\nlog what was truncated"]
    E --> D
    D --> F["Return assembled prompt dict"]
```

---

### Task P1-T06 — LLM Client: Base Implementation

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T06 |
| **Estimate** | 4–5 hours |
| **Status** | To Do |
| **Depends On** | P1-T05 |

**Description:** Implement the LLM Client module with concrete provider implementations for at least OpenAI and Ollama (local fallback). The client must be **pluggable** so additional providers can be added in Phase 2 without modifying calling code.

**Acceptance Criteria:**
- [ ] Abstract base class `LLMClient` defines interface: `generate(prompt: dict, temperature: float) -> str`
- [ ] `OpenAIClient` uses the `openai` SDK; reads API key from `OPENAI_API_KEY` environment variable
- [ ] `OllamaClient` calls the local Ollama REST API at `http://localhost:11434/api/chat`
- [ ] Both clients implement exponential backoff retry (max 3 retries, 2x factor, 1s base delay)
- [ ] `--provider` flag selects the active client; startup validates availability with a clear error on failure
- [ ] All client code covered by unit tests using mocked HTTP responses (`unittest.mock` or `pytest-httpx`)

**Provider Comparison:**

| | OpenAI | Anthropic | Ollama |
|--|--------|-----------|--------|
| **Use case** | Evaluation and production | Alternative evaluation | Offline development |
| **Auth** | `OPENAI_API_KEY` env var | `ANTHROPIC_API_KEY` env var | No auth (local) |
| **Phase 1 priority** | Primary | Phase 2 | Dev fallback |
| **Rate limits** | Yes — retry needed | Yes — retry needed | No |

---

### Task P1-T07 — Graduated Test Suite: Trivial Cases

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T07 |
| **Estimate** | 4–5 hours |
| **Status** | To Do |
| **Depends On** | P1-T02, P1-T04, P1-T06 |

**Description:** Build the first tier of the graduated test suite — trivial-complexity scenarios. Each is a single-resource Terraform file with one well-known misconfiguration, paired with a manually compiled ground-truth JSON threat list.

**Test Scenarios:**

| ID | Terraform Resource | Planted Misconfiguration | Expected STRIDE Category |
|----|-------------------|--------------------------|--------------------------|
| `TRI-01` | `aws_s3_bucket` | `acl = "public-read"` | Information Disclosure |
| `TRI-02` | `aws_security_group` | Ingress `0.0.0.0/0` on port 22 | Elevation of Privilege |
| `TRI-03` | `aws_db_instance` | `publicly_accessible = true`, `skip_final_snapshot = true` | Information Disclosure, Tampering |
| `TRI-04` | `aws_iam_policy` | `Action: "*"`, `Resource: "*"` (wildcard admin) | Elevation of Privilege |
| `TRI-05` | `aws_lambda_function` | No VPC config; plaintext `API_KEY` in env var | Information Disclosure |

**Fixture File Layout:**

```
tests/fixtures/
├── tri_01/
│   ├── main.tf            # Terraform fixture
│   └── ground_truth.json  # Expected threat list
├── tri_02/ ...
├── tri_03/ ...
├── tri_04/ ...
└── tri_05/
    ├── main.tf
    └── ground_truth.json
```

**Acceptance Criteria:**
- [ ] Each scenario has a `.tf` fixture and corresponding `ground_truth.json`
- [ ] Integration test for each scenario runs the full pipeline (LLM calls **mocked**) and verifies: (1) output is valid JSON conforming to the threat schema, (2) at least one threat with the expected STRIDE category and correct component name is present
- [ ] Manual verification run (live LLM, not mocked) executed for all 5 scenarios; results recorded in `tests/results/phase1_manual_run.md`
- [ ] All 5 trivial scenarios achieve **Recall >= 0.80** on the live LLM run

---

### Task P1-T08 — CLI Wiring and End-to-End Smoke Test

| Attribute | Detail |
|-----------|--------|
| **Task ID** | P1-T08 |
| **Estimate** | 2–3 hours |
| **Status** | To Do |
| **Depends On** | P1-T01 through P1-T07 |

**Description:** Wire all Phase 1 modules through the CLI entry point and verify the full pipeline runs end-to-end. This task **closes Phase 1** by confirming the system is runnable as a CLI tool.

**Acceptance Criteria:**
- [ ] `python -m threatcli analyze --iac tests/fixtures/tri_01/main.tf --format text` completes without errors and prints a formatted threat list to stdout
- [ ] `--format json` with `--output /path/to/out.json` produces a valid, schema-conforming JSON file
- [ ] Non-existent file path prints a clear error message and exits with a non-zero exit code
- [ ] `python -m threatcli --help` prints usage information for all commands and flags
- [ ] CI run (GitHub Actions) executes the full test suite (unit + mocked integration) and passes on the `main` branch

**End-to-End Test Flow:**

```mermaid
flowchart TD
    A["pytest tests/e2e/test_smoke.py"] --> B["Run: threatcli analyze\n--iac tri_01/main.tf\n--format text"]
    B --> C{Exit code == 0?}
    C -->|No| FAIL1["FAIL: unexpected error"]
    C -->|Yes| D["Parse stdout\ncheck for STRIDE keywords"]
    D --> E{Valid output?}
    E -->|No| FAIL2["FAIL: malformed output"]
    E -->|Yes| F["Run: threatcli analyze\n--format json\n--output /tmp/out.json"]
    F --> G["json.loads(out.json)"]
    G --> H{Valid JSON schema?}
    H -->|No| FAIL3["FAIL: schema violation"]
    H -->|Yes| PASS["PASS"]
```

---

## 6. Phase 1 — Task Summary

```mermaid
graph LR
    T01["P1-T01\nProject Skeleton\n2-3 hrs"]
    T02["P1-T02\nHCL Parser\n4-6 hrs"]
    T03["P1-T03\nJSON Serialiser\n2-3 hrs"]
    T04["P1-T04\nPrompt Templates\n3-4 hrs"]
    T05["P1-T05\nContext Builder\n3-4 hrs"]
    T06["P1-T06\nLLM Client\n4-5 hrs"]
    T07["P1-T07\nTest Suite\n4-5 hrs"]
    T08["P1-T08\nCLI Wiring\n2-3 hrs"]

    T01 --> T02
    T02 --> T03
    T03 --> T04
    T03 --> T05
    T04 --> T05
    T05 --> T06
    T04 --> T07
    T02 --> T07
    T06 --> T07
    T07 --> T08
```

| Task ID | Title | Estimate | Depends On | Status |
|---------|-------|----------|------------|--------|
| P1-T01 | Project Skeleton and Environment Setup | 2–3 hrs | — | To Do |
| P1-T02 | HCL Parser: Core Resource Extraction | 4–6 hrs | P1-T01 | To Do |
| P1-T03 | HCL Parser: JSON Summary Serialiser | 2–3 hrs | P1-T02 | To Do |
| P1-T04 | STRIDE Prompt Templates (IaC-Only) | 3–4 hrs | P1-T03 | To Do |
| P1-T05 | Context Builder (IaC-Only Mode) | 3–4 hrs | P1-T03, P1-T04 | To Do |
| P1-T06 | LLM Client: Base Implementation | 4–5 hrs | P1-T05 | To Do |
| P1-T07 | Graduated Test Suite: Trivial Cases | 4–5 hrs | P1-T02, P1-T04, P1-T06 | To Do |
| P1-T08 | CLI Wiring and End-to-End Smoke Test | 2–3 hrs | P1-T01–P1-T07 | To Do |
| | **Total Estimate** | **24–33 hrs** | | |

---

## 7. Technical Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| `python-hcl2` fails to parse complex Terraform syntax (e.g. `for_each`, `dynamic` blocks) | Medium | High | Pin to stable release. Implement raw-text fallback extractor. Scope Phase 1 fixtures to avoid complex expressions. |
| LLM API rate limits slow evaluation runs | High | Medium | Cache API responses locally during development. Use Ollama for fast iteration; cloud API only for final evaluation. |
| LLM output does not conform to the required JSON schema | Medium | High | Retry-with-correction strategy: if parsing fails, re-submit the prompt with the parse error appended, asking the model to correct its format. |
| Token budget exceeded by large Terraform codebases | Medium | Medium | Truncation logic in P1-T05. Phase 1 fixtures are deliberately small. Chunking for larger files is a Phase 2 concern. |
| Hallucination rate exceeds 10% target | Medium | High | Grounding instructions in P1-T04 are specifically designed to mitigate this. Hallucination measurement is built into the evaluation framework from the start. |

---

*Document end. Phase 2 (Design Document Ingestion and Context Fusion) tasks will be added following Phase 1 completion.*
