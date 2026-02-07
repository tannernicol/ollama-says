.PHONY: run benchmark report demo clean test generate redact-check help

help: ## Show this help
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-16s %s\n", $$1, $$2}'

run: ## Run the full evaluation suite in simulate mode
	python scripts/evaluate.py --config config/suite.yaml --policy config/policy.yaml --simulate

benchmark: ## Run benchmark with regression comparison
	cd "$(CURDIR)" && python scripts/benchmark.py --config config/suite.yaml --simulate --compare reports/

report: ## Generate HTML report from latest run
	python scripts/evaluate.py --config config/suite.yaml --simulate --out reports
	python scripts/render_report.py --input reports/latest.json --output reports/latest.html
	@echo "Report written to reports/latest.html"

demo: ## Run the demo harness (no Ollama needed)
	python scripts/demo.py --config config/suite.yaml

generate: ## Generate a new suite YAML config
	python scripts/generate_cases.py --out config/suite.generated.yaml

test: ## Run the test suite
	python -m pytest tests/ -v

redact-check: ## Check for PII leakage in the repo
	python scripts/redact.py --self-check

clean: ## Remove generated reports
	rm -rf reports/*.json reports/*.html reports/*.md reports/*.jsonl
