# Defense Playbook

A practical guide to defending LLM applications against prompt injection, tool abuse, and data exfiltration.

## Design Controls

### Instruction/Data Separation
- Keep system prompts and user data in separate channels
- Never concatenate untrusted input directly into system instructions
- Use structured message formats (system/user/assistant roles)

### Tool Allowlists
- Define an explicit allowlist of permitted tools
- Reject any tool invocation not on the allowlist
- Scope tool permissions to minimum necessary

### Input Sanitization
- Normalize unicode characters before processing
- Strip or escape markup delimiters in user input
- Detect and flag encoded content (base64, hex, HTML entities)

### Output Validation
- Scan model output for credential patterns before returning
- Check for tool invocation syntax in text responses
- Apply blocklist/allowlist policy rules

## Detection Controls

### Signal-Based Monitoring
- Deploy all 8 signal detectors on production output
- Set severity thresholds per deployment context
- Alert on critical signals (exfiltration, secret_leakage)

### Policy Enforcement
- Define blocklist terms that trigger automatic rejection
- Define allowlist terms that indicate safe refusal behavior
- Log all policy decisions for audit

### Audit Logging
- Log every prompt, response, and policy decision
- Include: prompt_id, model, policy_version, signals, decision, timestamp
- Retain logs for incident investigation and regression analysis

## Operational Controls

### Red-Team Testing
- Run the full Ollama Says suite against every model version
- Include custom cases specific to your deployment context
- Schedule regular benchmark runs (weekly or per-release)

### Regression Detection
- Use benchmark mode to compare against previous baselines
- Flag any category score decrease as a regression
- Block deployment if critical regressions are detected

### Incident Response
- Define escalation paths for critical signal triggers
- Maintain a runbook for common injection patterns
- Post-mortem all successful injection attempts

## Implementation Checklist

- [ ] Instructions/data split enforced
- [ ] Tool calls scoped and gated
- [ ] Input sanitization in place
- [ ] Output validation in place
- [ ] Signal detectors deployed
- [ ] Policy rules configured
- [ ] Audit trail preserved end-to-end
- [ ] Red-team suite running on schedule
- [ ] Regression detection in CI/CD
