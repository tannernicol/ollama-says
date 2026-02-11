# Contributing

Thanks for your interest in Ollama Says.

## Getting Started

```bash
pip install -r requirements.txt pytest
make test
python scripts/evaluate.py --config config/suite.yaml --simulate
```

## Pull Requests

1. Fork the repo and create a focused branch.
2. Include test cases for new detectors or attack vectors.
3. Run `make test` before opening a PR.
4. Keep examples synthetic — no real credentials or proprietary prompts.

## Security

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities.
