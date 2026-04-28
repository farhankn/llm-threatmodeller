# ACSE-Eval Live Benchmark Comparison Report

**Date:** 2026-04-28  
**Project:** `llm-threatmodeller`  
**Target benchmark:** ACSE-Eval (Munshi et al., 2025, arXiv:2505.11565v2)

## 1. Objective

Create an updated live benchmark report using the newly generated Gemini Pro full-run file and preserve historical runs for comparison.

## 2. Result Relocation

Moved existing result sets into separate folders:
- Legacy full run (Gemini Flash Lite, zero-output run): `tests/results/history/2026-04-28-gemini-flash-lite-zero/acse_live_eval_gemini.json`
- Gemini Pro subset run (3 scenarios): `tests/results/history/2026-04-28-gemini-pro-subset3`

New full-run artifact copied from `/tmp`:
- `tests/results/current/2026-04-28-gemini-pro-full-retry/acse_live_eval_gemini_pro_retry.json`

## 3. Run Comparison Snapshot

| Run | Total | Success | Failed | Threats Generated | Ground Truth | Micro Precision | Micro Recall | Micro F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Legacy full (Flash Lite) | 100 | 100 | 0 | 0 | 618 | 0.0000 | 0.0000 | 0.0000 |
| Pro subset (3 scenarios) | 3 | 3 | 0 | 22 | 38 | 0.0455 | 0.0263 | 0.0333 |
| Pro full retry | 100 | 74 | 26 | 532 | 857 | 0.0301 | 0.0187 | 0.0230 |

## 4. Key Findings

1. The previous **0-threat issue is resolved** in Gemini Pro runs (subset: `22` threats, full retry: `532` threats).
2. The full retry run is **partially successful** (`74/100`), with `26` failed scenarios.
3. Failure root cause observed: `NameError(_llm_debug_enabled)` in `26` scenarios (captured during that run artifact).
4. Precision/recall remain low, so this is progress on generation robustness, not yet on benchmark quality.

## 5. Artifact Index

- Legacy summary: `tests/results/acse_eval_summary.json`
- Subset summary: `tests/results/history/2026-04-28-gemini-pro-subset3/acse_subset3_eval_summary.json`
- New full-run summary: `tests/results/current/2026-04-28-gemini-pro-full-retry/acse_live_eval_gemini_pro_retry_summary.json`
- New full-run report: `tests/results/current/2026-04-28-gemini-pro-full-retry/acse_live_eval_gemini_pro_retry_report.md`

## 6. Bottom Line

The new Gemini Pro full-run artifact demonstrates that the hard `0 generated threats` failure mode has been fixed for successful scenarios. The benchmark still needs quality improvements (and a clean 100/100 execution) before claiming strong ACSE-Eval parity.
