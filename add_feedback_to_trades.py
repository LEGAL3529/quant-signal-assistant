import pandas as pd

df = pd.read_csv("trades.csv")

# Простая логика: положительный PnL = успех (1), иначе (0)
df["feedback_15m"] = (df["pnl"] > 0).astype(int)
df["feedback_1h"] = (df["pnl"] > 0).astype(int)
df["feedback_4h"] = (df["pnl"] > 0).astype(int)

df.to_csv("trades.csv", index=False)
print("✅ Feedback columns added to trades.csv")
