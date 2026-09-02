# Detection Result — Unauthorized Cross-User Agent Tool Invocation

Detection file:
`detections/splunk/unauthorized_tool_userid_mismatch.spl`

Result:
4 detection hits.

Detected run IDs:
- 5d271363-2f52-4fb5-8c45-4e3af634362e
- dc0735e3-42ec-4b73-bec4-6a15cb6543d8
- b13a76bb-09ea-41d5-bc23-30aa02ae41ae
- 39c5bb81-18ca-49a8-a894-f96f1e7059c3

Explanation:
The authenticated user was userId 1, but the agent called `GetUserTransactions` with `action_input=2`.
