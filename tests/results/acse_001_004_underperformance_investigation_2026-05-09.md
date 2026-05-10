# ACSE 001 & 004 Underperformance Investigation

Date: 2026-05-09

## Scope

Investigated low-scoring scenarios `acse_001` and `acse_004` with targeted live reruns and prompt/model variants.

## Baseline (Prompt v1)

Model: `gemini-3.1-pro-preview`, temperature `0.0`, include docs = true

- `ACSE_001_R1`: TP=1 FP=6 FN=10, Precision=0.143, Recall=0.091
- `ACSE_004_R1`: TP=1 FP=6 FN=14, Precision=0.143, Recall=0.067

## Root Cause Findings

1. Component canonicalization drift
- Model often emitted component identifiers as short/bare names (for example `iam_roles`, `amazon_efs`) instead of strict Terraform identifiers (`resource_type.resource_name`).
- This reduced exact identity overlap and increased false positives.

2. Threat targeting drift
- Threats were often plausible but attached to adjacent components instead of the benchmark's expected component (for example infrastructure-adjacent control rather than designated primary component).

3. STRIDE category drift
- Some threats used defensible but non-benchmark category assignments, reducing TP under strict category+component matching.

## Prompt Tweak (v2)

Updated `prompts/system_multisource.txt` to enforce:
- Exact `component` contract (`resource_type.resource_name` only)
- No bare/display labels
- Single best-fit STRIDE category per threat (reduced duplicate category inflation)
- Stronger evidence requirements and explicit severity values

## Results After Prompt v2

Model: `gemini-3.1-pro-preview`, temperature `0.0`, include docs = true

- `ACSE_001_R1`: TP=3 FP=3 FN=8, Precision=0.500, Recall=0.273
- `ACSE_004_R1`: TP=3 FP=3 FN=12, Precision=0.500, Recall=0.200

Change vs baseline:
- `acse_001`: Precision +0.357, Recall +0.182
- `acse_004`: Precision +0.357, Recall +0.133

## Code-Level Optimization Pass (v3)

Implemented:
- Multisource chunk-selection fix: resource map is now passed into chunk scoring.
- Better resource-keyword extraction (including ACSE tag aliases) for design chunk relevance.
- Deterministic component alignment to canonical Terraform IDs before output.
- Duplicate threat suppression by `(component, stride_category)`.

Results:

- `gemini-3.1-pro-preview`, temp `0.0`
  - `acse_001`: TP=4 FP=2 FN=7, Precision=0.667, Recall=0.364
  - `acse_004`: TP=4 FP=2 FN=11, Precision=0.667, Recall=0.267

- `gemini-2.5-pro`, temp `0.0`
  - `acse_001`: TP=5 FP=3 FN=6, Precision=0.625, Recall=0.455
  - `acse_004`: TP=5 FP=3 FN=10, Precision=0.625, Recall=0.333

- `gemini-2.5-pro`, temp `0.2`
  - `acse_001`: TP=5 FP=3 FN=6, Precision=0.625, Recall=0.455
  - `acse_004`: TP=6 FP=4 FN=9, Precision=0.600, Recall=0.400

## Model Variant Sweep

Prompt v1:
- `gemini-2.5-pro`
  - `acse_001`: P=0.000, R=0.000
  - `acse_004`: P=0.188, R=0.200
- `gemini-2.5-flash-lite`
  - `acse_001`: P=0.000, R=0.000
  - `acse_004`: P=0.000, R=0.000

Prompt v2:
- `gemini-2.5-pro`
  - `acse_001`: TP=6 FP=2 FN=5, Precision=0.750, Recall=0.545
  - `acse_004`: TP=4 FP=4 FN=11, Precision=0.500, Recall=0.267

## Recommendation

Best observed setup on these two scenarios after the full optimization pass:
- Prompt: `system_multisource.txt` v2 (current)
- Model: `gemini-2.5-pro`
- Temperature: `0.2` (best Recall on `acse_004` while keeping Precision stable)

This combination delivered the strongest Precision/Recall trade-off in this targeted investigation.

## Artifacts

- Consolidated results directory:
  - `tests/results/current/2026-05-09-acse-001-004-tuning/`
- Key files:
  - `acse_14_baseline_eval_env.json`
  - `acse_14_g25pro_eval.json`
  - `acse_14_g25flashlite_eval.json`
  - `acse_14_promptv2_eval.json`
  - `acse_14_g25pro_promptv2_eval.json`
  - `acse_004_g25pro_promptv2_eval.json`
  - `acse_14_opt2_g31_eval.json`
  - `acse_14_opt2_g25pro_eval.json`
  - `acse_14_opt3_g25pro_eval.json`
  - `acse_14_opt3_g25pro_t02_eval.json`
- Threat logs per run:
  - `tests/results/current/2026-05-09-acse-001-004-tuning/logs/`
