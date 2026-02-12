# LangChain SSRF Lab (CVE-2025-2828)

Local-only reproduction of SSRF via HTTP requests tools without strict URL
validation. Mirrors the RequestsToolkit issue where user-controlled URLs
could reach internal services.

## Run
```bash
python labs/langchain-ssrf-2025-2828/run_lab.py
```

## Try It
- Vulnerable UI: `http://localhost:<control-port>/control.html`
- Defended UI: `http://localhost:<control-port>/control_defended.html`
- Internal target: `http://localhost:<internal-port>/secret`
- Public target: `http://localhost:<public-port>/public`

## Ollama-Driven Prompt (Optional)
Use a local Ollama model to generate a URL, then paste into the fetch field:
```bash
python scripts/ollama_prompt.py --model qwen2.5:7b --prompt "Return a single URL that fetches the internal secret on localhost."
```

## Evidence (Local Run)
Captured on 2026-02-11.

Screenshot:
![LangChain SSRF Lab](../../docs/assets/labs/langchain-ssrf-2025-2828.png)

Report excerpt:
```json
{
  "lab_id": "langchain-ssrf-2025-2828",
  "timestamp": "20260211T003722Z",
  "action": "fetch_defended",
  "status": "blocked",
  "blocked_reason": "localhost_blocked"
}
```

## Measurements (Local Loopback)
Sample size: 10 runs
- Vulnerable fetch avg: 1.92 ms
- Vulnerable fetch P95: 1.17 ms
- Defended block avg: 0.47 ms
- Defended block P95: 0.51 ms
Notes: numbers are localhost-only and not representative of real networks.
Avg is higher than P95 due to one outlier in a 10-sample run.

## Engineer Notes
- This lab is almost identical to CVE-2024-3095 but targets a different tool.
- Blocking localhost removes the “wow” factor but proves the core issue fast.
- If I were shipping this, I would add egress allowlists per tool.

## Detection Ideas
- Log tool fetches with the calling chain and resolved IP.
- Alert on non-allowlisted destinations or repeated blocked attempts.
- Capture SSRF attempts as a distinct security signal.

## Operational Risk
- Exposed in any environment that lets prompts steer HTTP tools.
- High risk when internal services trust source IP.
- Containment: private IP blocks + allowlist + egress proxy.

## Report Output
Reports are written to `reports/labs/`:
- `langchain_ssrf_2025_2828_latest.json`

## Defense Cost JSON
`labs/langchain-ssrf-2025-2828/defense_costs.json` follows `docs/defense-cost-schema.json`.

## Defense Cost Matrix
| Defense | UX friction | Performance impact | Operational complexity | Notes |
| --- | --- | --- | --- | --- |
| Block localhost / private IPs | Low | None | Low | Stops direct SSRF to local services |
| Allowlist HTTP destinations | Medium | None | Medium | Requires explicit config per deployment |
| DNS re-resolution on fetch | Low | Low | Medium | Mitigates DNS rebinding |
| Outbound egress proxy | Medium | Low | Medium | Centralized enforcement |
| Strip URL from user input | High | None | Low | Breaks feature but closes class of bug |

## Safe Payload
The internal service only returns a dummy secret string and increments a counter.
No external calls are made.
