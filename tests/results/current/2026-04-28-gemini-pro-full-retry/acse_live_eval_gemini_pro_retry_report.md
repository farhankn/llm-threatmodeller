# ACSE-Eval Gemini Pro Retry Report

- Run ID: `run_20260428_134359`
- Timestamp: `2026-04-28T14:33:32.605274+00:00`
- Provider/Model: `gemini` / `gemini-2.5-pro`
- Scenarios: `74/100` succeeded

## Core Outcome

- The run no longer has the old `0-threat` issue: generated threats are non-zero.
- Total generated threats: `532`
- Failed scenarios: `26`

## Aggregate Metrics

- TP/FP/FN: `16` / `516` / `841`
- Micro precision: `0.0301`
- Micro recall: `0.0187`
- Micro F1: `0.0230`
- Mean precision: `0.0332`
- Mean recall: `0.0177`
- Mean hallucination rate: `0.9101`
- Mean STRIDE TFC recall: `0.5173`
- Mean MITRE TFC recall: `0.0000`

## Failure Breakdown

- `NameError(_llm_debug_enabled)`: `26` scenarios
