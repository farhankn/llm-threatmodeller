# Phase 1 Manual Run Results

## Run metadata

- **Date:** 2026-04-28
- **Scenario:** `TRI-01`
- **Command used:**

```bash
source .venv/bin/activate
set -a; source .env; set +a
python -m threatcli analyze \
  --iac tests/fixtures/tri_01/main.tf \
  --doc Design_Docs/design.md \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json \
  --output /tmp/tri01_live_output.json
```

- **Dataset reference (ground truth):** `tests/fixtures/tri_01/ground_truth.json`

## Input correlation

### IaC input (`tests/fixtures/tri_01/main.tf`)

```hcl
resource "aws_s3_bucket" "public_bucket" {
  bucket = "public-demo-bucket"
  acl    = "public-read"
}
```

### Ground-truth expectation (`tests/fixtures/tri_01/ground_truth.json`)

- 1 expected threat:
  - STRIDE: **Information Disclosure**
  - Component: **aws_s3_bucket.public_bucket**
  - Evidence: `acl = "public-read"`

This means the dataset expects a **single data-exposure finding** caused by public bucket ACL.

## Model output (live run)

The model produced **7 threats** (`T-001` .. `T-007`), including:
- 1 directly about public S3 exposure (Information Disclosure on `aws_s3_bucket.public_bucket`)
- additional items about tampering, CLI spoofing, LLM API disclosure, hallucination risk, DoS, and privilege escalation.

## Comparison against dataset

## Confusion counts

- **TP = 1** (correctly matched ground truth item)
- **FP = 6** (extra threats not in dataset target for TRI-01)
- **FN = 0** (no missed ground-truth threats)

## Calculations

- **Precision** = `TP / (TP + FP)` = `1 / (1 + 6)` = **0.1429** (14.29%)
- **Recall** = `TP / (TP + FN)` = `1 / (1 + 0)` = **1.0000** (100%)
- **F1** = `2PR / (P + R)` = `2 * 0.1429 * 1.0 / (0.1429 + 1.0)` = **0.2500**
- **Hallucination Rate** (project comparator) = `5 / 7` = **0.7143** (71.43%)
  - reason: 5 threats referenced components not present in IaC resource map (`CLI Tool.*`, `LLM API.*`)

## Threat-by-threat interpretation

| Threat ID | Model output meaning | Correlated to input? | Dataset status |
|---|---|---|---|
| T-001 | Public-read S3 can expose data | Yes (`acl = "public-read"`) | **TP (match)** |
| T-002 | Possible tampering on same bucket | Partial (same resource, but write path not shown in IaC) | FP |
| T-003 | Spoofing of CLI tool binary/process | No (outside TRI-01 IaC scope) | FP + hallucinated component |
| T-004 | Sensitive data leakage to LLM backend | No (meta-tool risk, not TRI-01 infra threat) | FP + hallucinated component |
| T-005 | Hallucination/inaccurate-output risk | No (quality-risk statement, not STRIDE infra finding) | FP + hallucinated component |
| T-006 | DoS against CLI pipeline | No (outside TRI-01 IaC scope) | FP + hallucinated component |
| T-007 | Privilege escalation in CLI runtime | No (outside TRI-01 IaC scope) | FP + hallucinated component |

## Key takeaway for report

For TRI-01, the model found the **correct core threat** (high recall), but added many out-of-scope/tool-level findings (low precision). In thesis terms: the run demonstrates strong detection of obvious IaC misconfiguration but weak scope control when broad design-context text is provided.

## Continued testing (TRI-01 to TRI-05 dataset comparison)

### Batch command used

```bash
source .venv/bin/activate
set -a; source .env; set +a
python -m threatcli evaluation run \
  --fixtures tests/fixtures/tri_01 \
  --fixtures tests/fixtures/tri_02 \
  --fixtures tests/fixtures/tri_03 \
  --fixtures tests/fixtures/tri_04 \
  --fixtures tests/fixtures/tri_05 \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --include-docs \
  --output /tmp/tri_live_eval_gemini.json
```

### Detailed comparison run

A second live pass was executed scenario-by-scenario to capture matched/extra/missed items against each fixture ground truth.

## Aggregate results (detailed live pass)

- Total scenarios: **5**
- Total expected threats (ground truth): **6**
- Total generated threats: **19**
- **TP = 5, FP = 14, FN = 1**
- **Micro Precision** = `5 / (5 + 14)` = **0.2632**
- **Micro Recall** = `5 / (5 + 1)` = **0.8333**
- **Micro F1** = `2PR/(P+R)` = **0.4000**
- **Macro Precision** = **0.2800**
- **Macro Recall** = **0.8000**
- **Mean Hallucination Rate** = **0.0000**

## Scenario-by-scenario correlation with input

| Scenario | IaC signal in input | Dataset expected threat(s) | Live model behavior | Result |
|---|---|---|---|---|
| TRI-01 | `aws_s3_bucket.public_bucket.acl = "public-read"` | Information Disclosure on `aws_s3_bucket.public_bucket` | Matched expected Info Disclosure; added Tampering + DoS on same component | TP=1 FP=2 FN=0 |
| TRI-02 | `aws_security_group.ssh_open.ingress.cidr_blocks = ["0.0.0.0/0"]` on port 22 | Elevation of Privilege on `aws_security_group.ssh_open` | Generated Spoofing + Information Disclosure + DoS; **missed EoP label** | TP=0 FP=3 FN=1 |
| TRI-03 | `aws_db_instance.app_db.publicly_accessible = true` and `skip_final_snapshot = true` | Information Disclosure + Tampering on `aws_db_instance.app_db` | Matched both expected threats; added DoS | TP=2 FP=1 FN=0 |
| TRI-04 | IAM policy with `Action="*"` and `Resource="*"` | Elevation of Privilege on `aws_iam_policy.wildcard_admin` | Matched expected EoP; added Spoofing + Tampering + Info Disclosure + DoS | TP=1 FP=4 FN=0 |
| TRI-05 | Lambda env var plaintext secret (`API_KEY = "plaintext-secret"`) | Information Disclosure on `aws_lambda_function.handler` | Matched expected Info Disclosure; added Spoofing + Tampering + DoS + EoP | TP=1 FP=4 FN=0 |

## What these metrics mean (quick interpretation)

- **Precision (low here):** Many generated findings were plausible but not in the fixture’s labeled target set for that scenario.
- **Recall (high here):** The model usually found the expected core threat(s).
- **F1:** Shows the balance; current runs are recall-heavy and precision-light.
- **Hallucination rate (0.0):** Extra findings still mapped to real IaC components, so they were over-predictions rather than fabricated components.

## Comparative takeaway

Across TRI-01..TRI-05, the model is strong at detecting obvious insecure IaC patterns but tends to over-generate additional STRIDE categories beyond the fixture labels. For report framing: this behavior supports a **high-sensitivity / lower-specificity** profile under current prompting and temperature settings.
