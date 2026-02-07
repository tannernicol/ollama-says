#!/usr/bin/env python3
"""Ollama Says — Demo harness.

Runs the evaluation suite in simulate mode and prints a summary.
Can be used without a running Ollama instance.
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

# Allow importing from the scripts directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import (
    compute_score,
    evaluate_case,
    load_cases,
    scores_by_category,
    simulated_response,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo harness for Ollama Says")
    parser.add_argument("--config", default="config/suite.yaml", help="Suite config YAML")
    parser.add_argument("--simulate", action="store_true", default=True, help="Use simulated responses (default)")
    args = parser.parse_args()

    suite, cases = load_cases(args.config)

    results: list[dict] = []
    for case in cases:
        case_id = case.get("id", "unknown")
        output = simulated_response(case_id)
        result = evaluate_case(case, output)
        results.append(result)

    score = compute_score(results)
    cat_scores = scores_by_category(results)

    report = {
        "suite": suite.get("name", "unknown"),
        "total_cases": len(cases),
        "defense_score": f"{score}/100",
        "passes": sum(1 for r in results if r["status"] == "pass"),
        "warns": sum(1 for r in results if r["status"] == "warn"),
        "fails": sum(1 for r in results if r["status"] == "fail"),
        "category_scores": {k: f"{v}/100" for k, v in cat_scores.items()},
        "cases": [
            {
                "id": r["id"],
                "status": r["status"],
                "signals": [s["id"] for s in r.get("signals", [])],
            }
            for r in results
        ],
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
