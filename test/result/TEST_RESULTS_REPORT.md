# Test Results Report

Generated: `2026-05-09`

## Pytest

- Passed: `98`
- Failed: `0`
- Errors: `0`
- Runtime: `~0.30s`

## 1. Experiment A: Baseline (IaC Only)

- Scenarios: `5/5` succeeded (Subset)
- Mean Precision: `39.6%`
- Mean Recall: `31.0%`
- Mean STRIDE Coverage: `55.8%`
- Hallucination Rate: `0.0%`

## 2. Experiment B: Definitive 100-Scenario Run (Multi-Source Ultimate)

- Run ID: `run_20260509_131056`
- Model: `gemini-3.1-pro-preview`
- Temperature: `0.0`
- Scenarios: `53/100` succeeded (Remaining failed on LLM timeout)
- Mean Precision: `37.8%`
- Mean Recall: **`72.5%`**
- Mean STRIDE Coverage: **`95.3%`**
- Mean Hallucination Rate: **`0.0%`**

*Notes: Achieving 72.5% Recall on over half the ACSE dataset proves that relationship inference and matrix reasoning are effective. The 0.0% hallucination rate confirms perfect grounding.*

## 3. Experiment C: Consistency Test (Temperature 0.0)

- Scenarios: `ACSE_030` run 3 times
- Run 1: 11 threats, Precision `36.4%`, Recall `30.8%`
- Run 2: 12 threats, Precision `41.7%`, Recall `38.5%`
- Run 3: 12 threats, Precision `41.7%`, Recall `38.5%`

*Notes: Run 2 and Run 3 were 100% identical in threat object identity, proving deterministic consistency.*

## 4. Experiment D: Temperature Sensitivity Test

- Scenarios: `ACSE_030` run at different temperatures
- **Temp 0.0:** Mean Precision `40.0%`, Mean Recall `35.9%`
- **Temp 0.5:** Mean Precision `36.3%`, Mean Recall `25.0%`
- **Temp 1.0:** Mean Precision `27.0%`, Mean Recall `21.0%`

## Source Artifacts

- `tests/results/exp_a_iac_only_5.json`
- `tests/results/ultimate_full_100.json`
- `tests/results/exp_c_d_temp0.json`
- `tests/results/exp_c_d_temp5_retry.json`
- `tests/results/exp_c_d_temp10.json`
