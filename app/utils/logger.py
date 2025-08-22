import os
import json
from datetime import datetime

LOG_PATH = "./data/logs/mom_session_log.json"

def log_event(event_dict):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    event_dict["logged_at"] = datetime.now().isoformat()
    try:
        logs = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        logs.append(event_dict)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        pass  # logging failed silently

def get_logs():
    if not os.path.exists(LOG_PATH): return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
