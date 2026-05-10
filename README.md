# Threat Model CLI

Threat Model CLI is a Python command line tool that analyzes Terraform IaC and generates STRIDE-aligned threat findings with LLM providers.

## CLI Interface Preview

```bash
$ threatcli analyze --iac main.tf --doc design.md

[Information Disclosure]
- T-001 (Critical) aws_s3_bucket.data: Public read access enabled.
- T-002 (High) aws_s3_bucket.data: Server-side encryption is disabled.
  !! DISCREPANCY: Design chunk_004 requires 'AES-256 encryption'.

[Tampering]
- T-003 (Medium) aws_s3_bucket.data: Versioning is not enabled.
  !! DISCREPANCY: Design chunk_009 requires 'Immutable storage'.

Summary: 4 threats identified (2 discrepancies).
```

## Installation

1. Ensure you have Python 3.10+.
2. Create a virtual environment.
3. Install the project in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage (Placeholder)

```bash
python -m threatcli --help
python -m threatcli analyze --iac path/to/main.tf --format text
python -m threatcli analyze --iac path/to/main.tf --provider gemini --format json
python -m threatcli analyze --iac path/to/main.tf --provider gemini --format pdf --output threat-report.pdf
python -m threatcli analyze --iac path/to/main.tf --doc design.md --doc-dir docs/ --format json
python -m threatcli evaluation run --fixtures tests/fixtures --provider gemini --model gemini-2.5-flash-lite --include-docs --threat-log-dir evaluation/results/threat_logs --output evaluation/results/latest_run.json
python -m threatcli evaluation import-acse --dataset acse_eval_export.json --output-root tests/fixtures/acse
python -m threatcli evaluation import-acse --dataset data/acse_eval/train_0.parquet --resolve-paths --output-root tests/fixtures/acse
```

More commands and providers are implemented incrementally.

## Documentation artifacts in `Design_Docs`

- `Design_Docs/implementation-changes-summary.md`: full implementation summary of recent delivered features.
- `Design_Docs/chapter-4-implementation-addendum.md`: extra Chapter 4 (Implementation) content you can merge into the dissertation/paper PDF.
- `Design_Docs/chapter-4-implementation-issues-challenges-decisions.md`: chapter-ready write-up of implementation issues, engineering challenges, and design decisions.

## Generated data / benchmark artifacts

ACSE and evaluation outputs are intentionally ignored in git by default:

- `data/acse_eval/`
- `tests/fixtures/acse/`
- `evaluation/results/`

### Document ingestion controls

- `--doc`: include one or more specific `.md` / `.txt` files
- `--doc-dir`: include all `.md` / `.txt` files under a directory
- `--max-doc-tokens`: cap total document tokens ingested (default `15000`)
- `--max-chunk-tokens`: control chunk size (default `1500`)
- `--overlap-tokens`: control chunk overlap (default `100`)

### Evaluation extras

- `--threat-log-dir`: dump per-scenario generated threat logs (and errors) as JSON during `evaluation run`
- Evaluation run output now includes:
  - per-scenario `jaccard_index` (output-vs-ground-truth threat identity overlap)
  - aggregate `mean_jaccard_index`
  - aggregate pairwise repeat-run Jaccard stats (`mean_pairwise_jaccard`, min/max, pair count)

## Provider Configuration

- OpenAI: set `OPENAI_API_KEY`
- Gemini: set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)
- Ollama: run local server at `http://localhost:11434`

For Vertex API-key usage with Gemini, set:

- `GEMINI_API_MODE=vertex`
- `GEMINI_BASE_URL=https://aiplatform.googleapis.com` (optional override in code path if exposed)
- Use a Vertex-supported model name (for example `gemini-2.5-flash-lite`)

You can also load keys from files using:

- `OPENAI_API_KEY_FILE`
- `GEMINI_API_KEY_FILE`
- `GOOGLE_API_KEY_FILE`

Each `*_FILE` variable should point to a local file containing only the key text.

Example local setup:

```bash
cp .env.example .env
# edit .env, then:
export $(grep -v '^#' .env | xargs)
```
