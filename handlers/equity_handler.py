import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_equity_plot():
    try:
        df = pd.read_csv("trades.csv")

        if "pnl" not in df.columns:
            raise ValueError("Missing 'pnl' column in trades.csv")

        df["equity"] = df["pnl"].cumsum()

        plt.figure(figsize=(10, 5))
        plt.plot(df["equity"], label="Equity Curve")
        plt.title("Equity Growth Over Time")
        plt.xlabel("Trade #")
        plt.ylabel("Equity")
        plt.grid(True)
        plt.legend()

        path = "equity_curve.png"
        plt.savefig(path)
        plt.close()

        return path
    except Exception as e:
        print(f"[EQUITY ERROR] {e}")
        return None
