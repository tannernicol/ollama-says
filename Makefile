.PHONY: demo evaluate generate report

demo:
	python scripts/demo.py --config config/example.yaml

evaluate:
	python scripts/evaluate.py --config config/suite.yaml --policy config/policy.yaml --simulate

generate:
	python scripts/generate_cases.py --out config/suite.generated.yaml

report:
	python scripts/render_report.py --input reports/latest.json --output reports/latest.html
