"""Evaluation runner for batch scenario experiments."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any

from threatcli.evaluation.comparator import compare, load_ground_truth, load_llm_output
from threatcli.parsers.iac_parser import parse_iac


def discover_fixtures(paths: list[Path]) -> list[Path]:
    fixtures: set[Path] = set()
    for base in paths:
        if base.is_file():
            if base.name == "ground_truth.json":
                fixtures.add(base.parent.resolve())
            continue
        if not base.exists():
            continue
        for gt in base.rglob("ground_truth.json"):
            fixture_dir = gt.parent.resolve()
            if (fixture_dir / "main.tf").exists():
                fixtures.add(fixture_dir)
    return sorted(fixtures)


def collect_doc_files(fixture_path: Path) -> list[Path]:
    docs: list[Path] = []
    for pattern in ("*.md", "*.txt"):
        docs.extend(sorted(fixture_path.glob(pattern)))
    return [p for p in docs if p.name not in {"ground_truth.json"}]


def _mean_or_zero(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(mean(values))


def run_experiment(
    fixtures: list[Path],
    provider: str,
    model: str | None,
    temperature: float,
    include_docs: bool,
    repeats: int,
) -> dict[str, Any]:
    run_id = f"run_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    scenario_results: list[dict[str, Any]] = []

    for repeat in range(repeats):
        for fixture in fixtures:
            scenario_id = f"{fixture.name.upper()}_R{repeat + 1}"
            with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
                output_path = Path(tmp.name)
            command = [
                sys.executable,
                "-m",
                "threatcli",
                "analyze",
                "--iac",
                str(fixture / "main.tf"),
                "--provider",
                provider,
                "--format",
                "json",
                "--temperature",
                str(temperature),
                "--output",
                str(output_path),
            ]
            if model:
                command.extend(["--model", model])
            if include_docs:
                for doc in collect_doc_files(fixture):
                    command.extend(["--doc", str(doc)])

            started = time.monotonic()
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            latency_seconds = time.monotonic() - started

            if completed.returncode != 0:
                scenario_results.append(
                    {
                        "scenario_id": scenario_id,
                        "fixture_path": str(fixture),
                        "exit_code": completed.returncode,
                        "error": (completed.stderr or completed.stdout).strip(),
                        "latency_seconds": round(latency_seconds, 3),
                    }
                )
                continue

            llm_output = load_llm_output(output_path)
            ground_truth = load_ground_truth(fixture / "ground_truth.json")
            resource_map = parse_iac([fixture / "main.tf"])
            metrics = compare(llm_output, ground_truth, resource_map)
            scenario_results.append(
                {
                    "scenario_id": scenario_id,
                    "fixture_path": str(fixture),
                    "threats_generated": len(llm_output),
                    "ground_truth_threats": len(ground_truth),
                    "tp": metrics["tp"],
                    "fp": metrics["fp"],
                    "fn": metrics["fn"],
                    "precision": metrics["precision"],
                    "recall": metrics["recall"],
                    "ddr": metrics["ddr"],
                    "hallucination_rate": metrics["hallucination_rate"],
                    "matched_discrepancies": metrics["matched_discrepancies"],
                    "planted_discrepancies": metrics["planted_discrepancies"],
                    "exit_code": 0,
                    "latency_seconds": round(latency_seconds, 3),
                }
            )

    successful = [item for item in scenario_results if item.get("exit_code") == 0]
    aggregate = {
        "mean_precision": _mean_or_zero([item["precision"] for item in successful]),
        "mean_recall": _mean_or_zero([item["recall"] for item in successful]),
        "mean_ddr": _mean_or_zero([item["ddr"] for item in successful]),
        "mean_hallucination_rate": _mean_or_zero([item["hallucination_rate"] for item in successful]),
        "total_scenarios": len(scenario_results),
        "successful_scenarios": len(successful),
        "failed_scenarios": len(scenario_results) - len(successful),
        "total_threats_generated": sum(item["threats_generated"] for item in successful),
        "total_ground_truth_threats": sum(item["ground_truth_threats"] for item in successful),
    }

    return {
        "run_id": run_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "include_docs": include_docs,
        "repeats": repeats,
        "scenario_results": scenario_results,
        "aggregate": aggregate,
    }


def write_run_result(result: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
