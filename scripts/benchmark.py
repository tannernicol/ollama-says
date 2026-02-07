#!/usr/bin/env python3
"""Ollama Says — Benchmark mode.

Runs the full suite against a model, calculates aggregate scores per
category, compares against previous runs for regression detection, and
outputs a benchmark scorecard.
"""
import argparse
import json
import time
from pathlib import Path

import yaml

from evaluate import (
    SEVERITY_ORDER,
    compute_score,
    evaluate_case,
    load_cases,
    scores_by_category,
    simulated_response,
    call_ollama,
)


def find_previous_report(reports_dir: Path) -> dict | None:
    """Find the most recent benchmark report in *reports_dir*."""
    candidates = sorted(reports_dir.glob("benchmark_*.json"), reverse=True)
    for path in candidates:
        try:
            return json.loads(path.read_text())
        except Exception:
            continue
    return None


def trend_arrow(current: int, previous: int | None) -> str:
    """Return a text arrow indicating improvement, regression, or no change."""
    if previous is None:
        return "(new)"
    diff = current - previous
    if diff > 0:
        return f"(+{diff} improved)"
    elif diff < 0:
        return f"({diff} regressed)"
    return "(unchanged)"


def run_benchmark(
    config_path: str,
    model_override: str | None = None,
    simulate: bool = False,
    reports_dir: str = "reports",
) -> dict:
    """Execute the benchmark and return the full report dict."""
    suite, cases = load_cases(config_path)
    model_cfg = suite.get("model", {})
    endpoint = model_cfg.get("endpoint", "http://localhost:11434")
    model_name = model_override or model_cfg.get("name", "qwen2.5:7b")

    results: list[dict] = []
    for case in cases:
        case_id = case.get("id", "unknown")
        if simulate:
            output = simulated_response(case_id)
        else:
            output = call_ollama(endpoint, model_name, case.get("prompt", ""))
        result = evaluate_case(case, output)
        results.append(result)

    overall = compute_score(results)
    cat_scores = scores_by_category(results)

    # --- Compare with previous run ---
    out_dir = Path(reports_dir)
    previous = find_previous_report(out_dir)
    prev_overall = previous["summary"]["score"] if previous else None
    prev_cats = previous["summary"].get("category_scores", {}) if previous else {}

    regressions: list[str] = []
    comparisons: dict[str, dict] = {}
    for cat, score in cat_scores.items():
        prev_score = prev_cats.get(cat)
        arrow = trend_arrow(score, prev_score)
        comparisons[cat] = {
            "score": score,
            "previous": prev_score,
            "trend": arrow,
        }
        if prev_score is not None and score < prev_score:
            regressions.append(f"{cat}: {prev_score} -> {score}")

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    summary = {
        "suite": suite.get("name"),
        "model": model_name,
        "total": len(results),
        "passes": sum(1 for r in results if r["status"] == "pass"),
        "warns": sum(1 for r in results if r["status"] == "warn"),
        "fails": sum(1 for r in results if r["status"] == "fail"),
        "score": overall,
        "category_scores": cat_scores,
        "generated_at": timestamp,
    }

    report = {
        "summary": summary,
        "comparisons": comparisons,
        "regressions": regressions,
        "overall_trend": trend_arrow(overall, prev_overall),
        "results": results,
    }

    # --- Write report ---
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"benchmark_{timestamp}.json"
    report_path.write_text(json.dumps(report, indent=2))

    return report


def print_scorecard(report: dict) -> None:
    """Print a human-readable benchmark scorecard to stdout."""
    summary = report["summary"]
    comparisons = report.get("comparisons", {})
    regressions = report.get("regressions", [])
    trend = report.get("overall_trend", "")

    print("=" * 60)
    print("  OLLAMA SAYS — BENCHMARK SCORECARD")
    print("=" * 60)
    print(f"  Suite:   {summary['suite']}")
    print(f"  Model:   {summary['model']}")
    print(f"  Cases:   {summary['total']}")
    print(f"  Date:    {summary['generated_at']}")
    print("-" * 60)
    print(f"  OVERALL DEFENSE SCORE: {summary['score']}/100  {trend}")
    print(f"  Pass: {summary['passes']}  Warn: {summary['warns']}  Fail: {summary['fails']}")
    print("-" * 60)
    print("  CATEGORY SCORES:")
    for cat, info in sorted(comparisons.items()):
        score = info["score"]
        cat_trend = info["trend"]
        bar = "#" * (score // 5) + "." * (20 - score // 5)
        print(f"    {cat:<20s} [{bar}] {score:>3d}/100  {cat_trend}")
    print("-" * 60)

    if regressions:
        print("  REGRESSIONS DETECTED:")
        for reg in regressions:
            print(f"    !! {reg}")
    else:
        print("  No regressions detected.")

    print("=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark prompt injection defenses and compare against previous runs.",
    )
    parser.add_argument("--config", default="config/suite.yaml", help="Suite config YAML")
    parser.add_argument("--model", help="Override model name from config")
    parser.add_argument("--simulate", action="store_true", help="Use simulated responses")
    parser.add_argument("--compare", default="reports", help="Directory with previous benchmark reports")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of scorecard")
    args = parser.parse_args()

    report = run_benchmark(
        config_path=args.config,
        model_override=args.model,
        simulate=args.simulate,
        reports_dir=args.compare,
    )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_scorecard(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
