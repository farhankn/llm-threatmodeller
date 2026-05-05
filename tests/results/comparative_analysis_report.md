# Comparative Analysis Report

**Date:** 2026-05-04  
**Scope:** ACSE benchmark evolution across legacy and current Gemini runs.

## Runs Compared

1. `tests/results/history/2026-04-28-gemini-flash-lite-zero/acse_live_eval_gemini.json`
2. `tests/results/history/2026-04-28-gemini-pro-subset3/acse_subset3_live_eval_gemini_pro.json`
3. `tests/results/current/2026-04-28-gemini-pro-full-retry/acse_live_eval_gemini_pro_retry.json`
4. `tests/results/current/2026-05-04-gemini-3.1-pro-preview-full-100/run_full_100.json`

## Metric Comparison

| Metric | Legacy Full (Flash Lite) | Pro Subset (3) | Pro Full Retry | 3.1 Pro Preview Full (100) |
|---|---:|---:|---:|---:|
| Total scenarios | 100 | 3 | 100 | 100 |
| Successful scenarios | 100 | 3 | 74 | 100 |
| Failed scenarios | 0 | 0 | 26 | 0 |
| Total threats generated | 0 | 22 | 532 | 621 |
| Total ground-truth threats | 618 | 38 | 857 | 1152 |
| Micro precision | 0.0000 | 0.0455 | 0.0301 | 0.0338 |
| Micro recall | 0.0000 | 0.0263 | 0.0187 | 0.0182 |
| Micro F1 | 0.0000 | 0.0333 | 0.0230 | 0.0237 |
| Mean hallucination rate | 0.0000 | 0.9167 | 0.9101 | 0.9230 |
| Mean STRIDE TFC recall | n/a | 0.4519 | 0.5173 | 0.4883 |
| Mean MITRE TFC recall | n/a | 0.0000 | 0.0000 | 0.0000 |

## Summary

1. Reliability: the latest run completed 100/100 scenarios successfully.
2. Output generation: sustained non-zero threat generation at full benchmark scale.
3. Quality: recall/precision and MITRE coverage remain low and require targeted prompt/comparator improvements.
