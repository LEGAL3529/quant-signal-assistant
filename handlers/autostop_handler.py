import json
import os

AUTOSTOP_FILE = "autostop_config.json"

def set_autostop_limit(percent: float):
    try:
        config = {"drawdown_limit": percent}
        with open(AUTOSTOP_FILE, "w") as f:
            json.dump(config, f)
        return "Сохранено"
    except Exception as e:
        return f"Ошибка: {e}"

def get_autostop_limit():
    if os.path.exists(AUTOSTOP_FILE):
        with open(AUTOSTOP_FILE, "r") as f:
            return json.load(f).get("drawdown_limit", None)
    return None

def check_autostop(current_drawdown_percent: float):
    limit = get_autostop_limit()
    if limit is not None:
        return current_drawdown_percent >= limit
    return False
