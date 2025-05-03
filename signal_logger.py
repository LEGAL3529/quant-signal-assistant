import csv
import os
from datetime import datetime

LOG_PATH = "logs/signal_log.csv"

def log_signal(symbol, signal_type, confidence, sent=True):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["datetime", "symbol", "type", "confidence", "telegram_sent"])
        writer.writerow([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            signal_type,
            round(confidence, 4),
            sent
        ])
