import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

def generate_heatmap():
    try:
        df = pd.read_csv("trades.csv", parse_dates=["timestamp"])
        df["hour"] = df["timestamp"].dt.hour
        df["weekday"] = df["timestamp"].dt.day_name()
        df["pnl"] = df["pnl"].astype(float)

        pivot = df.pivot_table(index="weekday", columns="hour", values="pnl", aggfunc="sum").fillna(0)

        plt.figure(figsize=(12, 6))
        sns.heatmap(pivot, annot=True, fmt=".1f", cmap="coolwarm")
        plt.title("🔥 PnL Heatmap (Hour × Day)")
        plt.xlabel("Hour")
        plt.ylabel("Weekday")
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        return buf
    except Exception as e:
        print("[HEATMAP ERROR]", e)
        return None
