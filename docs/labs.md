# Labs

Local-only reproductions of real-world issues with safe payloads and explicit
comparisons between vulnerable and defended flows.

Use `docs/lab-template.md` when adding a new lab.

Render a lab report to HTML:
```
python scripts/render_lab_report.py --input reports/labs/<lab>_latest.json --output reports/labs/<lab>_latest.html
```

Run a quick local validation pass:
```
python scripts/run_all_labs.py
```

## OpenClaw Invite (CVE-2026-25253)
- Location: `labs/openclaw-invite/`
- Focus: invite link auto-connect leaks a gateway token to attacker endpoint,
  which then performs privileged actions.
- Safety: localhost-only, benign payload.
- Entry point: `python labs/openclaw-invite/run_lab.py`

## LangChain SSRF (CVE-2024-3095)
- Location: `labs/langchain-ssrf-2024-3095/`
- Focus: SSRF via URL fetch tool (WebResearchRetriever).
- Safety: localhost-only internal service.
- Entry point: `python labs/langchain-ssrf-2024-3095/run_lab.py`

## LangChain SSRF (CVE-2025-2828)
- Location: `labs/langchain-ssrf-2025-2828/`
- Focus: SSRF via HTTP requests tools (RequestsToolkit).
- Safety: localhost-only internal service.
- Entry point: `python labs/langchain-ssrf-2025-2828/run_lab.py`
