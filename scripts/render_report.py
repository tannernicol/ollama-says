#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--template", default="templates/report.html")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    summary = data.get("summary", {})
    results = data.get("results", [])

    rows = []
    for r in results:
        signals = ", ".join([s.get("id") for s in r.get("signals", [])]) or "—"
        status = r.get("status", "unknown")
        pill_class = "pill"
        if status == "fail":
            pill_class += " fail"
        elif status == "warn":
            pill_class += " warn"
        rows.append(
            f"<tr><td>{r.get('id')}</td><td><span class='{pill_class}'>{status}</span></td><td>{signals}</td><td>{r.get('expected_behavior')}</td></tr>"
        )

    template = Path(args.template).read_text()
    html = template
    html = html.replace("{{suite}}", str(summary.get("suite", "")))
    html = html.replace("{{generated_at}}", str(summary.get("generated_at", "")))
    html = html.replace("{{total}}", str(summary.get("total", "")))
    html = html.replace("{{fails}}", str(summary.get("fails", "")))
    html = html.replace("{{rows}}", "\n".join(rows))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
