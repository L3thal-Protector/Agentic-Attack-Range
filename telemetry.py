import json
import os
import uuid
from datetime import datetime, timezone

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent_tao.jsonl")

def _safe_string(value):
    try:
        return str(value)
    except Exception:
        return repr(value)

def _write_event(event):
    os.makedirs(LOG_DIR, exist_ok=True)
    event["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def write_tao_run(user_prompt, response):
    run_id = str(uuid.uuid4())

    _write_event({
        "event_type": "user_prompt",
        "run_id": run_id,
        "user_prompt": user_prompt
    })

    steps = response.get("intermediate_steps", [])

    for step_number, step in enumerate(steps, start=1):
        agent_action = step[0]
        observation = step[1]

        _write_event({
            "event_type": "tao_step",
            "run_id": run_id,
            "step_number": step_number,
            "thought_log": _safe_string(getattr(agent_action, "log", "")),
            "action": _safe_string(getattr(agent_action, "tool", "")),
            "action_input": _safe_string(getattr(agent_action, "tool_input", "")),
            "observation": _safe_string(observation)
        })

    _write_event({
        "event_type": "final_answer",
        "run_id": run_id,
        "final_answer": _safe_string(response.get("output", ""))
    })
