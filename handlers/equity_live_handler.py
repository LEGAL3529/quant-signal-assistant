import pandas as pd
import matplotlib.pyplot as plt

def generate_equity_live():
    df = pd.read_csv("trades.csv")

    if "pnl" not in df.columns:
        raise ValueError("Missing 'pnl' column in trades.csv")

    df["equity"] = df["pnl"].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(df["equity"])
    plt.title("Live Equity Curve")
    plt.xlabel("Trades")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.tight_layout()

    output_path = "equity_live.png"
    plt.savefig(output_path)
    plt.close()

    return output_path
