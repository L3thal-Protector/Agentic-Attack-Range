# Agentic Attack Range

Local AI security lab showing how a vulnerable LLM agent can be attacked through unsafe tool use, then detected in Splunk.

## Summary

This project tests a DVLA-style vulnerable LLM agent that retrieves user transaction data through backend tools. I added telemetry, performed controlled attacks, mapped the findings to MITRE ATLAS, and wrote Splunk detections for the malicious behavior.

Main attack pattern:

`Prompt injection -> unsafe tool call -> unauthorized userId access -> sensitive data leakage -> Splunk detection`

## Highlights

- Built and ran a local vulnerable AI agent with Streamlit and Ollama
- Added custom JSONL telemetry for prompts, actions, tool inputs, observations, and final answers
- Tested direct prompt injection, goal hijacking, tool misuse, and indirect prompt injection
- Mapped successful attacks to MITRE ATLAS
- Ingested agent logs into Splunk
- Wrote SPL detections that caught the attacks
- Saved screenshots and CSV exports as evidence

## Lab Stack

| Component | Used |
|---|---|
| LLM backend | Ollama `mistral-nemo` |
| App | DVLA-style vulnerable LLM agent |
| Frontend | Streamlit |
| Telemetry | Custom JSONL logs |
| SIEM | Splunk |
| Splunk index | `agentic_ai` |
| Sourcetype | `_json` |

## What I Built

The agent was modified to log activity into:

`logs/agent_tao.jsonl`

Each run records:

- user prompt
- run ID
- event type
- tool/action name
- action input
- tool observation
- final answer
- timestamp

This made it possible to investigate the agent like a security event source.

## Successful Attacks

The lab user was `userId 1`. The main vulnerability was that the agent could be manipulated into calling `GetUserTransactions` with `action_input=2`, causing cross-user data access.

| Attack ID | Attack | Result |
|---|---|---|
| AAR-002-003 | Tool misuse / cross-user boundary check | Successful |
| AAR-002-004 | Sensitive flag extraction | Successful |
| AAR-002-005 | Goal hijack using compliance-mode framing | Successful |
| AAR-002-006 | Indirect prompt injection through transaction data | Successful |

Evidence:

`evidence/phase2/`

Attack tracker:

`attacks/phase2_attack_tracker.csv`

## MITRE ATLAS Mapping

| Attack | Vector | Outcome |
|---|---|---|
| AAR-002-003 | AML.T0051.000 - Direct Prompt Injection | AML.T0086 - Exfiltration via AI Agent Tool Invocation |
| AAR-002-004 | AML.T0051.000 - Direct Prompt Injection | AML.T0086 - Exfiltration via AI Agent Tool Invocation |
| AAR-002-005 | AML.T0051.000 - Direct Prompt Injection | AML.T0086 - Exfiltration via AI Agent Tool Invocation |
| AAR-002-006 | AML.T0051.001 - Indirect Prompt Injection | AML.T0086 - Exfiltration via AI Agent Tool Invocation |

Mapping files:

- `mappings/atlas_mapping.md`
- `mappings/atlas_mapping.csv`

## Splunk Detections

Agent telemetry was uploaded to Splunk with:

- Index: `agentic_ai`
- Sourcetype: `_json`
- Host: `agentic-dvla-local`

### Detection 1 - Unauthorized Cross-User Tool Invocation

File:

`detections/splunk/unauthorized_tool_userid_mismatch.spl`

Detects when the current user is `userId 1`, but the agent calls `GetUserTransactions` for another user.

Result:

- 4 hits
- Caught all four successful attacks

Evidence:

- `screenshots/splunk_detection_hits/unauthorized_tool_userid_mismatch_hits.png`
- `detections/phase4_evidence/unauthorized_tool_userid_mismatch_results.csv`

### Detection 2 - Secret Leakage in Final Answer

File:

`detections/splunk/secret_leak_final_answer.spl`

Detects when the agent leaks the lab flag in its final response.

Result:

- 3 true hits

Evidence:

- `screenshots/splunk_detection_hits/secret_leak_final_answer_hits.png`
- `detections/phase4_evidence/secret_leak_final_answer_results.csv`

### Detection 3 - Prompt Injection / Goal Hijack Markers

File:

`detections/splunk/suspicious_prompt_injection_markers.spl`

Detects suspicious strings related to prompt injection, goal hijacking, and boundary testing.

Result:

- 7 hits

Evidence:

- `screenshots/splunk_detection_hits/suspicious_prompt_injection_markers_hits.png`
- `screenshots/splunk_detection_hits/suspicious_prompt_injection_markers_hits_part2.png`
- `screenshots/splunk_detection_hits/suspicious_prompt_injection_markers_hits_part3.png`
- `detections/phase4_evidence/suspicious_prompt_injection_markers_results.csv`

## Key Takeaway

The main issue was not just that the model followed a bad prompt. The bigger security failure was that the backend tool trusted the user ID chosen by the agent.

A safer design should:

- bind tool calls to the authenticated session user
- enforce authorization in backend code
- treat tool output and database content as untrusted
- filter sensitive values before final responses
- log agent actions and tool inputs
- alert when tool inputs do not match user context

## Skills Demonstrated

- AI agent security testing
- Prompt injection testing
- Indirect prompt injection testing
- Tool misuse analysis
- MITRE ATLAS mapping
- OWASP Agentic risk classification
- Splunk log ingestion
- SPL detection writing
- Security documentation

## Status

Completed:

- Phase 1 - Target setup and telemetry
- Phase 2 - Manual attacks
- Phase 3 - MITRE ATLAS mapping
- Phase 4 - Splunk detections
- Phase 5 - Documentation

## Attribution

Base vulnerable agent adapted from Damn Vulnerable LLM Agent by ReversecLabs. My work focused on telemetry, attack testing, MITRE ATLAS mapping, Splunk detections, evidence collection, and documentation.

## Note

This was performed only in a local vulnerable lab environment created for learning and portfolio demonstration.

