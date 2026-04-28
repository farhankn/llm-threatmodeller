# ACSE-Eval Live Benchmark Comparison Report

**Date:** 2026-04-28  
**Project:** `llm-threatmodeller`  
**Target benchmark:** ACSE-Eval (Munshi et al., 2025, arXiv:2505.11565v2)

## 1. Objective

Run the current CLI against the local ACSE fixture corpus and compare observed metrics with published ACSE-Eval baselines.

## 2. Test execution

## 2.1 Command used

```bash
source .venv/bin/activate
set -a; source .env; set +a
python -m threatcli evaluation run \
  --fixtures tests/fixtures/acse \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --output /tmp/acse_live_eval_gemini.json
```

## 2.2 Run result

- **Successful scenarios:** 100 / 100
- **Output artifact:** `tests/results/acse_live_eval_gemini.json`
- **Summary artifact:** `tests/results/acse_eval_summary.json`
- **Fixture quality artifact:** `tests/results/acse_fixture_quality.json`
- **Paper baseline artifact:** `tests/results/acse_paper_baselines.json`

## 3. Metrics and calculations

Project comparator formulas:
- `Precision = TP / (TP + FP)`
- `Recall = TP / (TP + FN)`
- `F1 = 2PR / (P + R)`
- `Hallucination Rate = hallucinated_count / total_output_count`

Observed aggregate counts:
- `TP = 0`, `FP = 0`, `FN = 618`
- `total_generated_threats = 0`
- `total_ground_truth_threats = 618`

Computed values:
- `Micro Precision = 0 / (0 + 0) = 0.0` (implementation returns 0 on zero denominator)
- `Micro Recall = 0 / (0 + 618) = 0.0`
- `Micro F1 = 0.0`
- `Mean Precision = 0.0`
- `Mean Recall = 0.0`
- `Mean Hallucination Rate = 0.0`
- `No-output scenarios = 100 / 100 (100%)`
- `Mean scenario latency = 0.541s` (median `0.529s`)

## 4. Comparison against ACSE-Eval paper baselines

From ACSE-Eval tables:
- STRIDE TFC (Gemini 2.5 Pro, IaC 0-shot): **96.2%**  
  (source: extracted paper text lines 300-308)
- MITRE ATT&CK TFC (Gemini 2.5 Pro, IaC 0-shot): **45.9%**  
  (source: extracted paper text lines 330-338)

Current run (this project on local ACSE fixtures):
- STRIDE-like recall proxy: **0.0%** (`0/618`)
- MITRE ATT&CK coverage: **not computable in current comparator pipeline** (and normalized fixtures do not retain MITRE labels)

Direct delta (STRIDE proxy):
- `0.0% - 96.2% = -96.2 percentage points`

## 5. Why this comparison currently collapses (data quality check)

Fixture diagnostics on `tests/fixtures/acse`:
- Placeholder Terraform files: **100 / 100 (100%)**
- `design.md` as Python diagram scripts: **100 / 100 (100%)**
- Normalized ground-truth threats with `component = "unknown.component"`: **618 / 618 (100%)**
- Normalized ground-truth threats with `stride_category = "Tampering"`: **618 / 618 (100%)**
- Source records with MITRE labels: **618 / 618**
- Normalized ground truth with MITRE labels: **0 / 618**

Interpretation:
1. The live benchmark execution is technically successful.
2. However, the imported ACSE fixtures in this repo are not fidelity-equivalent to the original benchmark setup.
3. Because IaC is placeholder-only and labels are collapsed during normalization, this run is **not an apples-to-apples performance comparison** with the paper.

## 6. Output produced

Generated outputs are saved and reproducible:
- `tests/results/acse_live_eval_gemini.json` (full 100-scenario run output)
- `tests/results/acse_eval_summary.json` (aggregate metrics)
- `tests/results/acse_fixture_quality.json` (fixture fidelity diagnostics)
- `tests/results/acse_paper_baselines.json` (paper baseline values used for comparison)

## 7. Bottom line

I performed the ACSE-Eval test and produced a full comparison output.  
**Result:** the current local ACSE fixture representation yields 0 generated threats across all scenarios, so quantitative comparison against published ACSE-Eval numbers is currently invalid for model-quality claims and should be reported as a **dataset/ingestion fidelity limitation**, not as an LLM capability result.

