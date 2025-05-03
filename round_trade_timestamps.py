import pandas as pd

df = pd.read_csv("trades.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.floor("min")
df.to_csv("trades.csv", index=False)
print("✅ timestamps округлены до минут")
