import csv
from pathlib import Path

LOG_PATH = Path("logs/signal_log.csv")

def get_last_signals(n=10):
    if not LOG_PATH.exists():
        return ["No logs found."]
    
    with open(LOG_PATH, "r") as f:
        lines = list(csv.reader(f))
    
    header, rows = lines[0], lines[1:]
    if not rows:
        return ["No signals logged yet."]
    
    last_rows = rows[-n:]
    messages = []
    for row in last_rows:
        dt, symbol, sig_type, conf, sent = row
        messages.append(f"{dt} | {symbol} | {sig_type} | {float(conf):.2%}")
    return messages
