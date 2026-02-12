# CVE Gallery

Grouped by exploit class with links to the local labs.

## Invite / Deep Link Abuse
- OpenClaw Invite Link RCE — `labs/openclaw-invite/`

## SSRF via Tooling
- LangChain WebResearchRetriever SSRF — `labs/langchain-ssrf-2024-3095/`
- LangChain RequestsToolkit SSRF — `labs/langchain-ssrf-2025-2828/`

## Why This Set
- Covers link-based token leakage and tool-driven SSRF, two patterns that show up repeatedly in AI agents.
- Each lab is local-only but demonstrates real-world preconditions and defenses.
- Every lab has a screenshot, measurements, and a local JSON report.

## Local Validation
To quickly validate everything:
```
python scripts/run_all_labs.py
```
