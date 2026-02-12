# CVE-2024-3095 — LangChain WebResearchRetriever SSRF

## Summary
LangChain’s WebResearchRetriever accepted user-controlled URLs without
sufficient validation, allowing SSRF to internal services.

## Why This Lab
SSRF is an evergreen class, but this one is especially relevant for AI tool
chains because the model can synthesize URLs from untrusted input. It’s a good
demo of how “harmless” retrieval turns into a network pivot.

## Affected / Fixed
- Affected: versions before the fix (see advisory)
- Fixed: version listed in the advisory

## Operational Risk
- Any tool that follows model-supplied URLs is in scope.
- High risk in environments with metadata endpoints or internal APIs.
- Defense needs both URL validation and egress controls.

## Lab
- Local lab: `labs/langchain-ssrf-2024-3095/`
- Run: `python labs/langchain-ssrf-2024-3095/run_lab.py`

## Results (Local)
- Evidence: `labs/langchain-ssrf-2024-3095/README.md` includes a run excerpt and screenshot.
- Render report: `python scripts/render_lab_report.py --input reports/labs/langchain_ssrf_2024_3095_latest.json --output reports/labs/langchain_ssrf_2024_3095_latest.html`

## References
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2024-3095
- GitLab Advisory: https://advisories.gitlab.com/pkg/pypi/langchain/CVE-2024-3095/
