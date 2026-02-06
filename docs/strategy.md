# Defense + Detection Strategy

A practical approach for mitigating prompt injection in production systems.

## Layer 1: Design Controls
- Separate instructions from data inputs
- Use strict templates with fixed roles
- Explicitly constrain tool access

## Layer 2: Policy Controls
- Refusal policies for sensitive actions
- Human approval for destructive actions
- Audit logs for every tool call

## Layer 3: Detection Controls
- Regex and heuristic detection on outputs
- Blocklisted phrases and override patterns
- Secret redaction filters

## Layer 4: Operational Controls
- Red-team test suites and regression tests
- Change management for model upgrades
- On-call playbooks for suspected compromise
