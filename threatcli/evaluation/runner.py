"""Evaluation runner for batch scenario experiments."""

from __future__ import annotations

import json
import os
import shlex
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
    progress: bool = False,
    debug: bool = False,
    progress_file: Path | None = None,
) -> dict[str, Any]:
    run_id = f"run_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    scenario_results: list[dict[str, Any]] = []
    total_scenarios = len(fixtures) * repeats
    progress_enabled = _is_flag_enabled(progress, "TM_EVAL_PROGRESS")
    debug_enabled = _is_flag_enabled(debug, "TM_EVAL_DEBUG")

    _progress(
        f"Run {run_id} starting: total={total_scenarios}, provider={provider}"
        + (f", model={model}" if model else ""),
        enabled=progress_enabled,
    )
    _write_progress_snapshot(
        progress_file=progress_file,
        payload={
            "run_id": run_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "provider": provider,
            "model": model,
            "total_scenarios": total_scenarios,
            "completed_scenarios": 0,
            "successful_scenarios": 0,
            "failed_scenarios": 0,
            "last_scenario_id": None,
            "last_exit_code": None,
            "last_error": None,
        },
    )

    for repeat in range(repeats):
        for fixture_index, fixture in enumerate(fixtures):
            scenario_id = f"{fixture.name.upper()}_R{repeat + 1}"
            scenario_number = (repeat * len(fixtures)) + fixture_index + 1
            _progress(
                f"[{scenario_number}/{total_scenarios}] Starting {scenario_id} ({fixture}) with provider={provider}"
                + (f", model={model}" if model else "")
                + f", include_docs={include_docs}, temperature={temperature}",
                enabled=progress_enabled,
            )
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

            if debug_enabled:
                quoted = " ".join(shlex.quote(part) for part in command)
                _progress(
                    f"[DEBUG] {scenario_id} command: {quoted}",
                    enabled=True,
                )

            started = time.monotonic()
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            latency_seconds = time.monotonic() - started

            if completed.returncode != 0:
                error_text = (completed.stderr or completed.stdout).strip()
                if debug_enabled and error_text:
                    _progress(
                        f"[DEBUG] {scenario_id} error: {_truncate(error_text)}",
                        enabled=True,
                    )
                _progress(
                    f"[{scenario_number}/{total_scenarios}] Failed {scenario_id} "
                    f"(exit {completed.returncode}, {latency_seconds:.2f}s)",
                    enabled=progress_enabled,
                )
                scenario_results.append(
                    {
                        "scenario_id": scenario_id,
                        "fixture_path": str(fixture),
                        "exit_code": completed.returncode,
                        "error": error_text,
                        "latency_seconds": round(latency_seconds, 3),
                    }
                )
                _write_progress_snapshot(
                    progress_file=progress_file,
                    payload={
                        "run_id": run_id,
                        "timestamp": datetime.now(UTC).isoformat(),
                        "provider": provider,
                        "model": model,
                        "total_scenarios": total_scenarios,
                        "completed_scenarios": len(scenario_results),
                        "successful_scenarios": sum(
                            1 for item in scenario_results if item.get("exit_code") == 0
                        ),
                        "failed_scenarios": sum(
                            1 for item in scenario_results if item.get("exit_code") != 0
                        ),
                        "last_scenario_id": scenario_id,
                        "last_exit_code": completed.returncode,
                        "last_error": _truncate(error_text),
                    },
                )
                continue

            llm_output = load_llm_output(output_path)
            ground_truth = load_ground_truth(fixture / "ground_truth.json")
            resource_map = parse_iac([fixture / "main.tf"])
            metrics = compare(llm_output, ground_truth, resource_map)
            _progress(
                f"[{scenario_number}/{total_scenarios}] Finished {scenario_id} ({latency_seconds:.2f}s): "
                f"threats={len(llm_output)} gt={len(ground_truth)} "
                f"tp={metrics['tp']} fp={metrics['fp']} fn={metrics['fn']}"
                f" precision={metrics['precision']:.3f} recall={metrics['recall']:.3f}"
                f" stride_tfc={metrics['stride_tfc_recall']:.3f} mitre_tfc={metrics['mitre_tfc_recall']:.3f}",
                enabled=progress_enabled,
            )
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
                    "stride_tfc_tp": metrics["stride_tfc_tp"],
                    "stride_tfc_total": metrics["stride_tfc_total"],
                    "stride_tfc_recall": metrics["stride_tfc_recall"],
                    "mitre_tfc_tp": metrics["mitre_tfc_tp"],
                    "mitre_tfc_total": metrics["mitre_tfc_total"],
                    "mitre_tfc_recall": metrics["mitre_tfc_recall"],
                    "matched_discrepancies": metrics["matched_discrepancies"],
                    "planted_discrepancies": metrics["planted_discrepancies"],
                    "exit_code": 0,
                    "latency_seconds": round(latency_seconds, 3),
                }
            )
            _write_progress_snapshot(
                progress_file=progress_file,
                payload={
                    "run_id": run_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "provider": provider,
                    "model": model,
                    "total_scenarios": total_scenarios,
                    "completed_scenarios": len(scenario_results),
                    "successful_scenarios": sum(1 for item in scenario_results if item.get("exit_code") == 0),
                    "failed_scenarios": sum(1 for item in scenario_results if item.get("exit_code") != 0),
                    "last_scenario_id": scenario_id,
                    "last_exit_code": 0,
                    "last_error": None,
                },
            )

    successful = [item for item in scenario_results if item.get("exit_code") == 0]
    total_stride_tp = sum(item["stride_tfc_tp"] for item in successful)
    total_stride = sum(item["stride_tfc_total"] for item in successful)
    total_mitre_tp = sum(item["mitre_tfc_tp"] for item in successful)
    total_mitre = sum(item["mitre_tfc_total"] for item in successful)
    aggregate = {
        "mean_precision": _mean_or_zero([item["precision"] for item in successful]),
        "mean_recall": _mean_or_zero([item["recall"] for item in successful]),
        "mean_ddr": _mean_or_zero([item["ddr"] for item in successful]),
        "mean_hallucination_rate": _mean_or_zero([item["hallucination_rate"] for item in successful]),
        "mean_stride_tfc_recall": _mean_or_zero([item["stride_tfc_recall"] for item in successful]),
        "mean_mitre_tfc_recall": _mean_or_zero([item["mitre_tfc_recall"] for item in successful]),
        "micro_stride_tfc_recall": (total_stride_tp / total_stride) if total_stride else 0.0,
        "micro_mitre_tfc_recall": (total_mitre_tp / total_mitre) if total_mitre else 0.0,
        "total_scenarios": len(scenario_results),
        "successful_scenarios": len(successful),
        "failed_scenarios": len(scenario_results) - len(successful),
        "total_threats_generated": sum(item["threats_generated"] for item in successful),
        "total_ground_truth_threats": sum(item["ground_truth_threats"] for item in successful),
    }

    _progress(
        f"Run {run_id} complete: {aggregate['successful_scenarios']}/{aggregate['total_scenarios']} "
        f"succeeded, total_threats_generated={aggregate['total_threats_generated']}",
        enabled=progress_enabled,
    )
    _write_progress_snapshot(
        progress_file=progress_file,
        payload={
            "run_id": run_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "provider": provider,
            "model": model,
            "total_scenarios": aggregate["total_scenarios"],
            "completed_scenarios": aggregate["total_scenarios"],
            "successful_scenarios": aggregate["successful_scenarios"],
            "failed_scenarios": aggregate["failed_scenarios"],
            "last_scenario_id": None,
            "last_exit_code": None,
            "last_error": None,
            "done": True,
        },
    )

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


def _progress(message: str, *, enabled: bool = False) -> None:
    if not enabled:
        return
    print(message, file=sys.stderr, flush=True)


def _write_progress_snapshot(progress_file: Path | None, payload: dict[str, Any]) -> None:
    if progress_file is None:
        return
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    progress_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _is_flag_enabled(cli_value: bool, env_name: str) -> bool:
    if cli_value:
        return True
    return os.getenv(env_name, "").strip() in {"1", "true", "TRUE", "yes", "on"}


def _truncate(text: str, limit: int = 600) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."
