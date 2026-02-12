#!/usr/bin/env python3
"""Minimal Ollama prompt helper.

Uses the local Ollama HTTP API to generate text for a prompt.
"""
import argparse
import json
import sys
from urllib.request import Request, urlopen


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a prompt to local Ollama")
    parser.add_argument("--model", default="qwen2.5:7b", help="Ollama model name")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--endpoint", default="http://localhost:11434/api/generate")
    args = parser.parse_args()

    payload = json.dumps({"model": args.model, "prompt": args.prompt}).encode("utf-8")
    req = Request(args.endpoint, method="POST", data=payload, headers={"Content-Type": "application/json"})

    try:
        with urlopen(req, timeout=30) as resp:
            output = []
            for line in resp:
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                chunk = data.get("response", "")
                if chunk:
                    output.append(chunk)
            text = "".join(output).strip()
            print(text)
            return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
