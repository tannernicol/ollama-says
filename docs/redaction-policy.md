# Redaction Policy

All content in this repo is checked for sensitive data before release.

## Remove or Replace
- Domains and hostnames (replace with `example.com` or `evil.test`)
- IP addresses (replace with `10.0.0.0` or `192.0.2.1`)
- Usernames and emails (replace with `user@example.com`)
- Tokens, API keys, secrets (remove entirely)
- Service-specific paths (use placeholders)

## Verification
- Run `scripts/redact.py --self-check` to scan for leaks
- Manually review diffs before pushing
- The CI pipeline runs redaction checks automatically
