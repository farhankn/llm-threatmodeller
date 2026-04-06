# Threat Model CLI

Threat Model CLI is a Python command line tool that analyzes Terraform IaC and generates STRIDE-aligned threat findings with LLM providers.

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
python -m threatcli analyze --iac path/to/main.tf --doc design.md --doc-dir docs/ --format json
```

More commands and providers are implemented incrementally.

### Document ingestion controls

- `--doc`: include one or more specific `.md` / `.txt` files
- `--doc-dir`: include all `.md` / `.txt` files under a directory
- `--max-doc-tokens`: cap total document tokens ingested (default `15000`)
- `--max-chunk-tokens`: control chunk size (default `1500`)
- `--overlap-tokens`: control chunk overlap (default `100`)

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
