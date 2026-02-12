# Use Cases

## Pre-Release Defense Check
Use before shipping an LLM feature or model update.

Inputs:
- Prompt suite
- Policy rules
- Target model

Outputs:
- Pass/fail summary
- Severity signals
- JSON report

Notes:
- Run in simulate mode for quick smoke tests.

## Defense Regression Tracking
Use on a schedule to catch safety drift.

Inputs:
- Baseline report
- New report
- Model version info

Outputs:
- Delta summary
- Risk notes
- Trend data

Notes:
- Archive JSON reports for auditability.

## Security Training Lab
Use to teach teams how prompt injection works and how to defend.

Inputs:
- Curated cases
- Scenario notes
- Expected behaviors

Outputs:
- Classroom report
- Mitigation notes
- Improvement checklist

Notes:
- Keep all cases synthetic and local-only.

## Exploit Reproduction Lab
Use to validate a real-world CVE in a safe local harness and document defenses.

Inputs:
- Local lab script
- Vulnerable and defended flows
- Cost matrix notes

Outputs:
- JSON report
- Defense tradeoff summary
- Repro steps for teammates

Notes:
- Keep payloads benign.
- Keep all endpoints on localhost.
