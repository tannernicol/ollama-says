# Contributing

Thanks for contributing to Ollama Says.

## Workflow

1. Fork the repository and create a focused branch.
2. Add/update tests and docs with the code change.
3. Run local validation before opening a PR.
4. Open a PR with clear security impact notes.

## Local Validation

```bash
make test
pre-commit run --all-files
python scripts/redact.py --self-check
python scripts/evaluate.py --config config/suite.yaml --simulate
```

## Pull Request Expectations

- Keep PRs focused and reproducible.
- Include test cases for new detectors, policies, or suite logic.
- Keep examples synthetic and non-sensitive.
- Do not include real credentials, private hosts, or proprietary prompts.

## Starter Tasks

- See docs/good-first-issues.md for contributor-friendly tasks with acceptance criteria.
- Follow docs/release-policy.md when preparing release-impacting changes.
