# CVE-2025-2828 — LangChain RequestsToolkit SSRF

## Summary
LangChain’s HTTP RequestsToolkit could be abused to fetch user-supplied URLs
without strict validation, enabling SSRF.

## Why This Lab
This is the “same class, different tool” case. It’s useful to show that fixes
can’t live in one component; every tool that touches the network needs guardrails.

## Affected / Fixed
- Affected: versions before the fix (see advisory)
- Fixed: version listed in the advisory

## Operational Risk
- Prompt-influenced tools can accidentally become SSRF agents.
- Attackers can probe internal networks without direct access.
- Defense needs deny-by-default network policy plus validation.

## Lab
- Local lab: `labs/langchain-ssrf-2025-2828/`
- Run: `python labs/langchain-ssrf-2025-2828/run_lab.py`

## Results (Local)
- Evidence: `labs/langchain-ssrf-2025-2828/README.md` includes a run excerpt and screenshot.
- Render report: `python scripts/render_lab_report.py --input reports/labs/langchain_ssrf_2025_2828_latest.json --output reports/labs/langchain_ssrf_2025_2828_latest.html`

## References
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2025-2828
- GitHub Advisory: https://github.com/advisories/GHSA-mh97-864m-9wqj
