# Comparative Analysis Report (Testing + Calculations)

**Date:** 2026-04-28  
**Project:** `llm-threatmodeller`  
**Purpose:** Generate a test-backed comparative analysis aligned with the thesis evaluation intent (including ACSE-Eval relevance).

## 1. Tests Executed

### Test A — Full automated test suite
- **Command:** `source .venv/bin/activate && pytest`
- **Result:** `91 passed in 0.31s`
- **Interpretation:** Codebase regression baseline is currently healthy.

### Test B — Evaluation runner execution probe (live path)
- **Command:**  
  `python -m threatcli evaluation run --fixtures tests/fixtures/tri_01 --provider openai --output /tmp/eval_probe.json`
- **Runner output:** `Evaluation run complete: 0/1 scenarios succeeded.`
- **Recorded scenario error:** `OPENAI_API_KEY is not set`
- **Interpretation:** Evaluation pipeline works end-to-end structurally, but live LLM benchmarking is blocked without provider credentials.

### Test C — ACSE import fidelity comparison (source vs normalized fixtures)
- **Method:** For all local ACSE fixtures (`tests/fixtures/acse/*`), compare:
  1. `source_record.json` (rich ACSE schema),
  2. normalized `ground_truth.json` used by comparator/evaluation.

## 2. Output Comparison Values

## 2.1 Corpus-level counts

| Metric | Value |
|---|---:|
| ACSE scenarios analyzed | 100 |
| Source threats (`source_record.json`) | 618 |
| Normalized threats (`ground_truth.json`) | 618 |
| Placeholder Terraform files (`main.tf`) | 100 / 100 |
| Python diagram scripts stored as `design.md` | 100 / 100 |

## 2.2 STRIDE distribution comparison

### Source (ACSE rich annotations)
- Spoofing: 133
- Tampering: 284
- Repudiation: 79
- Information Disclosure: 343
- Denial of Service: 115
- Elevation of Privilege: 195
- Other labels observed: Lateral Movement (1), Access Control (1), Resource Exhaustion (1)

### Normalized fixture ground truth
- Tampering: 618

**Key comparison finding:** STRIDE diversity in source collapses to a single category in normalized evaluation data.

## 2.3 Field-retention comparison

| Comparison metric | Formula | Value |
|---|---|---:|
| STRIDE retention rate | `stride_retention_matches / paired_items = 284 / 618` | **45.95%** |
| MITRE retention rate | `normalized_with_mitre / source_with_mitre = 0 / 618` | **0.00%** |
| Component specificity retention | `(normalized_threats - unknown_component) / source_component_like = (618-618)/618` | **0.00%** |
| Generic-description rate | `normalized_generic_description / normalized_threats = 541 / 618` | **87.54%** |
| Placeholder-IaC rate | `placeholder_terraform_scenarios / acse_scenarios = 100 / 100` | **100.00%** |
| Python-design-doc rate | `python_design_docs / acse_scenarios = 100 / 100` | **100.00%** |

## 2.4 Non-ACSE fixture sanity check

| Metric | Value |
|---|---:|
| Non-ACSE scenarios | 7 |
| Non-ACSE threats | 10 |
| Non-ACSE `discrepancy_flag=true` | 4 |

**Interpretation:** Custom non-ACSE fixtures still contain discrepancy labels, so DDR-style testing is possible there.

## 3. Calculation Notes

### 3.1 Precision / Recall / DDR / Hallucination formulas used by the project
- `Precision = TP / (TP + FP)`
- `Recall = TP / (TP + FN)`
- `DDR = matched_discrepancies / planted_discrepancies`
- `Hallucination Rate = hallucinated_count / total_output_count`

These formulas are implemented in:
- `threatcli/evaluation/metrics.py`
- `threatcli/evaluation/comparator.py`

### 3.2 Example calculation (from this report)
- **STRIDE retention:** `284 / 618 = 0.4595 = 45.95%`
- **MITRE retention:** `0 / 618 = 0.0 = 0.00%`

## 4. Comparative Conclusion (for thesis write-up)

1. **Testing status is good**: the project test suite is passing (`91 passed`).
2. **Evaluation framework exists**: precision/recall/DDR/hallucination metrics are implemented and runnable.
3. **ACSE-Eval comparison is currently data-limited**: imported ACSE fixtures lose most comparative signal (MITRE, component specificity, STRIDE diversity), and all IaC files are placeholders.
4. **Implication for your report**: you can report robust internal testing and metric support, but should explicitly state that **full ACSE-Eval benchmark comparability requires improving import fidelity first** (especially STRIDE/MITRE/component preservation and real IaC ingestion).

