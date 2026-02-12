# CVE-2026-25253 — OpenClaw/Clawdbot Invite Link RCE

## Summary
The Control UI trusted a `gatewayUrl` query parameter and auto-connected on load,
sending a stored gateway token to the provided endpoint. A crafted invite link
could exfiltrate the token, enabling the attacker to connect to the victim’s
local gateway and invoke privileged actions, resulting in 1-click RCE.

## Why This Lab
This is the cleanest example I’ve seen of “1-click RCE” where the entire chain
hinges on a UI convenience feature. It’s a good interview discussion because
the fix is simple but the consequences are severe.

## Affected / Fixed
- Affected: all versions before `2026.1.29`
- Fixed: `2026.1.29`

## Operational Risk
- User needs to click a link; no other permissions required.
- Impact scales with gateway privileges and local network access.
- Defense should focus on breaking implicit trust in URLs.

## Lab
- Local lab: `labs/openclaw-invite/`
- Run: `python labs/openclaw-invite/run_lab.py`

## Results (Local)
- Evidence: `labs/openclaw-invite/README.md` includes a run excerpt and screenshot.
- Render report: `python scripts/render_lab_report.py --input reports/labs/openclaw_invite_latest.json --output reports/labs/openclaw_invite_latest.html`

## References
- GitLab Advisory: https://advisories.gitlab.com/pkg/npm/clawdbot/CVE-2026-25253/
