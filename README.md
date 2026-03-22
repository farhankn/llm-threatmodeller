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
```

More commands and providers are implemented incrementally.

## Provider Configuration

- OpenAI: set `OPENAI_API_KEY`
- Gemini: set `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)
- Ollama: run local server at `http://localhost:11434`
