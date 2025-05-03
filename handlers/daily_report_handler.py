import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime, timedelta

def generate_daily_report():
    try:
        df = pd.read_csv("trades.csv", parse_dates=["timestamp"])
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)

        df = df[df["timestamp"] >= yesterday]
        if df.empty:
            return None, None

        df.sort_values("timestamp", inplace=True)
        df["equity"] = df["pnl"].cumsum()

        # Метрики
        pnl = df["pnl"].sum()
        winrate = (df["pnl"] > 0).mean() * 100
        expectancy = df["pnl"].mean()
        returns = df["pnl"]
        sharpe = (returns.mean() / returns.std()) * (len(returns) ** 0.5) if returns.std() != 0 else 0
        max_dd = (df["equity"].cummax() - df["equity"]).max()

        summary = {
            "PnL": pnl,
            "Winrate": winrate,
            "Expectancy": expectancy,
            "Sharpe": sharpe,
            "MaxDD": max_dd
        }

        # График
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["equity"], label="Equity (24h)")
        plt.title("📈 Equity Curve — Last 24h")
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.grid(True)
        plt.tight_layout()
        plt.legend()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        return summary, buf

    except Exception as e:
        print("[DAILY REPORT ERROR]", e)
        return None, None

