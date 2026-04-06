# ThreatCLI Demo Script (Multi-Case)

Use this script to demonstrate increasing capability from simple IaC analysis to advanced multi-document discrepancy detection.

---

## 1) Setup (once per shell)

```bash
cd /Users/farhan/Mainproject/code/llm-threatmodeller
source .venv/bin/activate
set -a
source .env
set +a
```

Recommended `.env`:

```bash
GEMINI_API_KEY=...
GEMINI_API_MODE=vertex
```

Optional quick sanity check:

```bash
python -m threatcli --help
```

---

## 2) Case A — IaC only: public S3 bucket

Input: `tests/fixtures/tri_01/main.tf`

```bash
python -m threatcli analyze \
  --iac tests/fixtures/tri_01/main.tf \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json
```

Highlight:
- `aws_s3_bucket.public_bucket`
- likely `Information Disclosure`

---

## 3) Case B — IaC only: SSH open to internet

Input: `tests/fixtures/tri_02/main.tf`

```bash
python -m threatcli analyze \
  --iac tests/fixtures/tri_02/main.tf \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format text
```

Highlight:
- `aws_security_group.ssh_open`
- likely `Elevation of Privilege`

---

## 4) Case C — IaC only: public DB

Input: `tests/fixtures/tri_03/main.tf`

```bash
python -m threatcli analyze \
  --iac tests/fixtures/tri_03/main.tf \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json
```

Highlight:
- `aws_db_instance.app_db`
- likely `Information Disclosure`/`Tampering`

---

## 5) Case D — IaC + one design doc (fusion path)

Inputs:
- IaC: `tests/fixtures/tri_01/main.tf`
- Design: `Design_Docs/design.md`

```bash
python -m threatcli analyze \
  --iac tests/fixtures/tri_01/main.tf \
  --doc Design_Docs/design.md \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json
```

Highlight:
- unstructured design + structured IaC in one prompt
- discrepancy-capable output schema

---

## 6) Case E — Dry-run (no LLM call)

```bash
python -m threatcli analyze \
  --iac tests/fixtures/tri_01/main.tf \
  --doc Design_Docs/design.md \
  --dry-run \
  --format json | head -n 80
```

Highlight:
- shows fused prompt payload directly
- works offline for architecture explanation

---

## 7) Case F — Advanced IaC + design mismatch scenario

Inputs:
- IaC: `tests/fixtures/adv_01/main.tf`
- Design: `tests/fixtures/adv_01/design.md`

```bash
python -m threatcli analyze \
  --iac tests/fixtures/adv_01/main.tf \
  --doc tests/fixtures/adv_01/design.md \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json
```

Highlight:
- multiple risky resources in one run
- least-privilege drift (`aws_iam_policy.wildcard_admin`)
- design intent conflicts (private DB/logs vs IaC reality)

---

## 8) Case G — Multiple design docs (repeat `--doc`)

Inputs:
- IaC: `tests/fixtures/adv_02/main.tf`
- Docs:
  - `tests/fixtures/adv_02/design-overview.md`
  - `tests/fixtures/adv_02/design-operations.txt`

```bash
python -m threatcli analyze \
  --iac tests/fixtures/adv_02/main.tf \
  --doc tests/fixtures/adv_02/design-overview.md \
  --doc tests/fixtures/adv_02/design-operations.txt \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format text
```

Highlight:
- multi-document fusion with repeated `--doc`
- policy constraints aggregated across docs

---

## 9) Case H — Discrepancy-only view (professor-friendly)

```bash
python -m threatcli analyze \
  --iac tests/fixtures/adv_01/main.tf \
  --doc tests/fixtures/adv_01/design.md \
  --discrepancies-only \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json
```

Highlight:
- only `discrepancy_flag=true` findings shown
- ideal to prove “design vs implementation” capability

---

## 10) Case I — Directory ingestion + token controls

```bash
python -m threatcli analyze \
  --iac tests/fixtures/adv_02/main.tf \
  --doc-dir tests/fixtures/adv_02 \
  --max-doc-tokens 3000 \
  --max-chunk-tokens 600 \
  --overlap-tokens 80 \
  --provider gemini \
  --model gemini-2.5-flash-lite \
  --format json
```

Highlight:
- `--doc-dir` auto-discovers `.md`/`.txt`
- tunable ingestion for larger real-world design sets

---

## 11) Suggested live presentation flow

1. Case E (dry-run): architecture and prompt fusion.
2. Case A: baseline IaC threating.
3. Case F: advanced IaC + design conflict.
4. Case H: discrepancy-only executive view.
5. Case I: scale story (`--doc-dir` + token controls).

---

## 12) Troubleshooting

If key is not loaded:

```bash
set -a; source .env; set +a
```

If Vertex auth fails:
- ensure key is active and not revoked
- ensure `GEMINI_API_MODE=vertex`
- verify model name is available to your key/project
