# ACSE Dataset - Full 100 Scenarios Evaluation Report

Generated: `2026-05-05`
Run ID: `run_20260505_095540`
Provider: `gemini`
Model: `gemini-3.1-pro-preview`
Temperature: `0.0`

## Scenario Overview

- **Total Scenarios**: 100
- **Successful Scenarios**: 98
- **Failed Scenarios**: 2

## Threat Generation Metrics

- **Total Threats Generated**: 781
- **Total Ground Truth Threats**: 1127
- **Mean Precision**: 0.367 (36.7%)
- **Mean Recall**: 0.252 (25.2%)
- **Mean Hallucination Rate**: 0.115 (11.5%)
- **Mean Discrepancy Detection Rate (DDR)**: 0.0% *(Note: Due to a lack of planted discrepancies in the specific ground truth dataset.)*

## Framework Coverage

- **Mean STRIDE Framework Coverage (Recall)**: 0.595 (59.5%)
- **Micro STRIDE Framework Coverage (Recall)**: 0.573 (57.3%)
- **Mean MITRE ATT&CK Coverage (Recall)**: 0.0% *(Note: Consistent with expected LLM baselines lacking explicit MITRE curation.)*

## Artifacts

- **Full JSON Output**: `tests/results/current/2026-05-04-gemini-3.1-pro-preview-full-100/run_full_100.json`
- **Progress Tracking**: `tests/results/current/2026-05-04-gemini-3.1-pro-preview-full-100/run_progress.json`