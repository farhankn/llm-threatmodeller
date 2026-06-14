# Test Strategy and Documentation

## Overview
The project follows a multi-layered testing strategy to ensure the reliability of the analysis pipeline and the accuracy of the evaluation metrics. Testing covers internal function logic, module integration, and end-to-end CLI workflows.

## Test Layers

### 1. Unit Tests (`tests/`)
- Focus on individual functions in isolation.
- Examples: `test_iac_parser.py`, `test_doc_parser.py`, `test_evaluation_metrics.py`.
- Ensure base logic (parsing, metric computation) is robust.

### 2. Integration Tests (`tests/`)
- Validate how modules interact with each other.
- Examples: `test_context_builder.py` (checks prompt assembly under token limits), `test_evaluation_comparator.py` (checks threat matching logic).

### 3. End-to-End Tests (`tests/e2e/`)
- Run the full CLI tool through the `Typer` test runner.
- Validate exit codes, output schemas, and stream handling.
- Use real model outputs (fixtures) to ensure the tool handles LLM variability correctly.

## Evaluation Harness
The tool includes a specialized evaluation runner (`threatcli/evaluation/runner.py`) for large-scale benchmarking against the **ACSE-Eval** dataset.
- **Scenarios**: 100 expert-reviewed AWS architecture scenarios.
- **Metrics**: Precision, Recall, Jaccard Index, Hallucination Rate, STRIDE Coverage.
- **Process**: Automates batch execution, result aggregation, and metric computation.

## Ground Truth Alignment
To ensure rigorous evaluation, the system implements a "Fuzzy Tail-Matching" algorithm in `comparator.py`. This allows the tool to map LLM-generated identifiers to ground-truth labels while accounting for Terraform type prefixes and natural language variability.

## Continuous Integration
The project uses GitHub Actions for continuous integration. Every pull request triggers:
- Full `pytest` suite execution.
- Baseline analysis smoke tests.
- Linting and type checking.

## Artifacts
- **Test Results**: Maintained in `test/result/TEST_RESULTS_REPORT.md`.
- **JSON Logs**: Per-scenario raw outputs and metrics are preserved for auditability.
