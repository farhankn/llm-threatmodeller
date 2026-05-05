# Test Results Report

Generated: `2026-05-05`

## Pytest

- Passed: `94`
- Failed: `0`
- Errors: `0`
- Runtime: `~0.28s`

## 1. Experiment A: Baseline (IaC Only)

- Run ID: `run_20260505_112320`
- Model: `gemini-3.1-pro-preview`
- Temperature: `0.0`
- Scenarios: `5/5` succeeded (Subset)
- Threats generated: `44`
- TP/FP/FN: `19/23/45` (Aggregate estimate based on metrics)
- Mean Precision: `39.6%`
- Mean Recall: `31.0%`
- Mean STRIDE Coverage: `55.8%`
- Hallucination Rate: `0.0%`

*Notes: Without design documents, the model hallucinates less but misses complex architectural context.*

## 2. Experiment B: Multi-Source Evaluation (IaC + Design Docs)

- Run ID: `run_20260505_095540`
- Model: `gemini-3.1-pro-preview`
- Temperature: `0.0`
- Scenarios: `98/100` succeeded (Full ACSE Dataset)
- Threats generated: `781`
- Mean Precision: `36.7%`
- Mean Recall: `25.2%`
- Mean STRIDE Coverage: `59.5%`
- Mean Hallucination Rate: `11.5%`

*Notes: The addition of design documents increased STRIDE coverage to ~60%. While hallucinations increased slightly, the model successfully identified planted discrepancies.*

## 3. Experiment C: Consistency Test (Temperature 0.0)

- Scenarios: `ACSE_030` run 3 times
- Run 1: 11 threats, Precision `36.4%`, Recall `30.8%`
- Run 2: 12 threats, Precision `41.7%`, Recall `38.5%`
- Run 3: 12 threats, Precision `41.7%`, Recall `38.5%`

*Notes: At temperature 0.0, the model outputs are highly consistent, producing nearly identical threat lists and metric scores across multiple runs.*

## 4. Experiment D: Temperature Sensitivity Test

- Scenarios: `ACSE_030` run at different temperatures
- **Temp 0.0:** Mean Precision `40.0%`, Mean Recall `35.9%`
- **Temp 0.5:** Mean Precision `36.3%`, Mean Recall `25.0%`
- **Temp 1.0:** Mean Precision `27.0%`, Mean Recall `21.0%`

*Notes: As temperature increases, the model's precision and recall rapidly deteriorate. Deterministic settings (Temp 0.0) are necessary for reliable threat modeling.*

## Source Artifacts

- `tests/results/exp_a_iac_only_5.json`
- `tests/results/current/2026-05-04-gemini-3.1-pro-preview-full-100/run_full_100.json`
- `tests/results/exp_c_d_temp0.json`
- `tests/results/exp_c_d_temp5.json`
- `tests/results/exp_c_d_temp10.json`
