import json
from pathlib import Path
from threatcli.renderer import render_pdf

with open('tests/results/deep_dive_001_raw.json') as f:
    threats = json.load(f)

pdf_bytes = render_pdf(threats, report_meta={
    "title": "Test Threat Report",
    "generated_at": "2026-05-09T12:00:00Z",
    "tool_version": "0.1.0",
    "provider": "gemini",
    "model": "gemini-3.1-pro-preview",
    "iac_inputs": ["tests/fixtures/acse/acse_001/main.tf"],
    "doc_inputs": ["tests/fixtures/acse/acse_001/design.md"]
})

Path('tests/results/test_manual_render.pdf').write_bytes(pdf_bytes)
print("PDF rendered successfully.")
