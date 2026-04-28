# Comparative Analysis Report

**Date:** 2026-04-28  
**Scope:** ACSE benchmark result evolution across legacy full run, subset run, and new Gemini Pro full retry.

## 1. Inputs Compared

1. `tests/results/history/2026-04-28-gemini-flash-lite-zero/acse_live_eval_gemini.json`
2. `tests/results/history/2026-04-28-gemini-pro-subset3/acse_subset3_live_eval_gemini_pro.json`
3. `tests/results/current/2026-04-28-gemini-pro-full-retry/acse_live_eval_gemini_pro_retry.json`

## 2. Comparative Metrics

| Metric | Legacy Full (Flash Lite) | Pro Subset (3) | Pro Full Retry |
|---|---:|---:|---:|
| Total scenarios | 100 | 3 | 100 |
| Successful scenarios | 100 | 3 | 74 |
| Failed scenarios | 0 | 0 | 26 |
| Total threats generated | 0 | 22 | 532 |
| Total ground-truth threats | 618 | 38 | 857 |
| Micro precision | 0.0000 | 0.0455 | 0.0301 |
| Micro recall | 0.0000 | 0.0263 | 0.0187 |
| Micro F1 | 0.0000 | 0.0333 | 0.0230 |
| Mean hallucination rate | 0.0000 | 0.9167 | 0.9101 |
| Mean STRIDE TFC recall | n/a | 0.4519 | 0.5173 |
| Mean MITRE TFC recall | n/a | 0.0000 | 0.0000 |

## 3. Interpretation

1. The project moved from a zero-output full run to non-zero output in Gemini Pro runs.
2. The full retry demonstrates scale behavior (100 scenarios) but includes failed scenarios from a runtime code-path issue in that run artifact.
3. Threat generation robustness improved, but accuracy metrics are still far below paper-level coverage baselines.
4. Next benchmark-quality target is clean execution (100/100 successful) followed by precision/recall and MITRE coverage improvements.

## 4. Recommended Next Step

Re-run the full Gemini Pro benchmark using the now-fixed runtime code and regenerate the `current` folder artifacts for a clean apples-to-apples comparison.
