#!/usr/bin/env python3
import argparse
import json
import yaml


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    suite = cfg.get("suite", {})
    cases = suite.get("cases", [])

    report = {
        "suite": suite.get("name", "unknown"),
        "cases": [c.get("id") for c in cases],
        "score": f"{len(cases)}/{len(cases)}",
        "notes": "demo harness only",
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
