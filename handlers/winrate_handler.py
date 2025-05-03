import csv
from pathlib import Path

LOG_PATH = Path("logs/signal_log.csv")

def calculate_winrate(threshold=0.6):
    if not LOG_PATH.exists():
        return "No signal logs found."

    with open(LOG_PATH, "r") as f:
        rows = list(csv.reader(f))[1:]  # skip header

    confirmed = [r for r in rows if "CONFIRMED" in r[2]]
    if not confirmed:
        return "No confirmed signals yet."

    wins = 0
    for r in confirmed:
        signal_type = r[2]
        confidence = float(r[3])
        if "BUY" in signal_type and confidence > threshold:
            wins += 1
        elif "SELL" in signal_type and confidence < (1 - threshold):
            wins += 1

    winrate = wins / len(confirmed)
    return f"✅ Confirmed: {len(confirmed)}\n🏆 Wins: {wins}\n📈 Winrate: {winrate:.2%}"
