# Detection Signals

This document lists practical indicators of prompt injection or tool misuse.

## High-Risk Signals
- System prompt disclosure or references
- Tool invocation attempts in output
- Credential or secret-like strings
- Requests to call external URLs or exfiltrate data

## Medium-Risk Signals
- Instruction overrides ("ignore previous", "system message")
- Attempts to disable safeguards or logs
- Requests to broaden tool permissions

## Recommended Logging Fields
- prompt_id
- model
- policy_version
- tool_calls (if any)
- redaction_hits
- decision (allow/refuse)
- timestamp
