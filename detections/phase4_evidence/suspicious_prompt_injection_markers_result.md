# Detection Result — Suspicious Prompt Injection or Goal Hijack Markers

Detection file:
`detections/splunk/suspicious_prompt_injection_markers.spl`

Result:
7 detection hits.

Explanation:
This detection searches prompts, tool observations, thought logs, and final answers for suspicious strings related to prompt injection, goal hijacking, boundary validation, and indirect prompt injection.

This detection is intentionally broader than the secret-leak detection. It catches both successful and partial/blocked suspicious behavior.
