import pandas as pd

def calculate_summary():
    try:
        df = pd.read_csv("trades.csv", parse_dates=["timestamp"])
        df.sort_values("timestamp", inplace=True)
        df["equity"] = df["pnl"].cumsum()

        # Основные метрики
        total_pnl = df["pnl"].sum()
        winrate = (df["pnl"] > 0).mean() * 100
        expectancy = df["pnl"].mean()

        returns = df["pnl"]
        sharpe = (returns.mean() / returns.std()) * (len(returns) ** 0.5) if returns.std() != 0 else 0
        max_drawdown = (df["equity"].cummax() - df["equity"]).max()

        return {
            "sharpe": round(sharpe, 2),
            "max_dd": round(max_drawdown, 2),
            "winrate": round(winrate, 2),
            "expectancy": round(expectancy, 2),
            "total_pnl": round(total_pnl, 2)
        }

    except Exception as e:
        return {"error": str(e)}
