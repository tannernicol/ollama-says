# Defense Playbook

## Design Controls
- Separate instructions from data
- Use explicit tool allowlists
- Enforce least-privilege tool scopes
- Normalize and sanitize retrieved content before use

## Detection Controls
- Input and output validation
- Response policy checks
- Audit logging of prompts and actions
- Flag instruction overrides and suspicious tool requests

## Operational Controls
- Red-team test suite
- Regression testing on model upgrades
- Monitoring for abnormal tool usage
- Require approvals for destructive or external actions

## Implementation Checklist
- Instructions/data split enforced
- Tool calls scoped and gated
- Output validation in place
- Audit trail preserved end-to-end
