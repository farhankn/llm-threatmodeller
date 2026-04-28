# ACSE Subset (3 Scenarios) Live Evaluation Report

- Run ID: `run_20260428_140454`
- Provider/Model: `gemini` / `gemini-2.5-pro`
- Timestamp: `2026-04-28T14:06:59.504892+00:00`
- Scenarios: `3/3` succeeded

## Key Result

This subset run no longer has the old zero-output failure mode: the model generated `22` threats across `3` scenarios.

## Aggregate Metrics

- Total ground-truth threats: `38`
- TP/FP/FN: `1` / `21` / `37`
- Micro precision: `0.0455`
- Micro recall: `0.0263`
- Micro F1: `0.0333`
- Mean precision: `0.0417`
- Mean recall: `0.0238`
- Mean hallucination rate: `0.9167`
- Mean STRIDE TFC recall: `0.4519`
- Mean MITRE TFC recall: `0.0000`
- Mean latency (s): `41.70`
- Median latency (s): `40.62`

## Scenario Breakdown

| Scenario | Latency (s) | Generated | Ground Truth | TP | FP | FN | Precision | Recall | STRIDE TFC | MITRE TFC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `ACSE_001_R1` | 44.94 | 6 | 11 | 0 | 6 | 11 | 0.000 | 0.000 | 0.455 | 0.000 |
| `ACSE_002_R1` | 40.62 | 8 | 13 | 0 | 8 | 13 | 0.000 | 0.000 | 0.615 | 0.000 |
| `ACSE_003_R1` | 39.53 | 8 | 14 | 1 | 7 | 13 | 0.125 | 0.071 | 0.286 | 0.000 |

## Progress Tracking Files

- Live run output: `tests/results/acse_subset3_live_eval_gemini_pro.json`
- Rolling progress snapshot: `tests/results/acse_subset3_progress.json`
- Aggregate summary: `tests/results/acse_subset3_eval_summary.json`
