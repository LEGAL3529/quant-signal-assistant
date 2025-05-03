import csv
from pathlib import Path

LOG_PATH = Path("logs/signal_log.csv")

def calculate_pnl(threshold=0.6):
    if not LOG_PATH.exists():
        return "No log file found."

    with open(LOG_PATH, "r") as f:
        rows = list(csv.reader(f))[1:]  # skip header

    confirmed = [r for r in rows if "CONFIRMED" in r[2]]
    if not confirmed:
        return "No confirmed trades yet."

    pnl = 0
    for r in confirmed:
        sig_type = r[2]
        conf = float(r[3])
        if "BUY" in sig_type and conf > threshold:
            pnl += 1
        elif "SELL" in sig_type and conf < (1 - threshold):
            pnl += 1
        else:
            pnl -= 1

    return f"💰 PnL (simulated): {pnl} % from {len(confirmed)} trades"
