#!/usr/bin/env python3
"""Render a lab JSON report into HTML."""
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a lab report from JSON")
    parser.add_argument("--input", required=True, help="Path to lab JSON report")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--template", default="templates/lab_report.html", help="HTML template path")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text())
    template_path = Path(args.template)
    if not template_path.exists():
        template_path = Path(__file__).resolve().parent.parent / args.template
    template = template_path.read_text()

    ports = data.get("ports", {})
    state = data.get("state", {})

    html = template
    html = html.replace("{{lab_id}}", str(data.get("lab_id", "")))
    html = html.replace("{{timestamp}}", str(data.get("timestamp", "")))
    html = html.replace("{{action}}", str(data.get("action", "")))
    html = html.replace("{{requested_url}}", str(data.get("requested_url", "")))
    html = html.replace("{{status}}", str(data.get("status", "")))
    html = html.replace("{{blocked_reason}}", str(data.get("blocked_reason", "")))
    html = html.replace("{{control_port}}", str(ports.get("control", "")))
    html = html.replace("{{internal_port}}", str(ports.get("internal", "")))
    html = html.replace("{{public_port}}", str(ports.get("public", "")))
    html = html.replace("{{internal_hits}}", str(state.get("internal_hits", "")))
    html = html.replace("{{last_request}}", str(state.get("last_request", "")))
    html = html.replace("{{last_blocked}}", str(state.get("last_blocked", "")))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
