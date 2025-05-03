import pandas as pd
import os

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

for symbol in symbols:
    df = pd.read_csv(f"datasets/{symbol}_history.csv", index_col=0, parse_dates=True)

    df["return"] = df["close"].pct_change()
    df["volatility"] = df["return"].rolling(window=10).std()
    df["sma_5"] = df["close"].rolling(window=5).mean()
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_ratio"] = df["sma_5"] / df["sma_20"]

    df["target"] = (df["close"].shift(-5) > df["close"]).astype(int)

    df.dropna(inplace=True)

    df.to_csv(f"datasets/{symbol}_features.csv")
    print(f"✅ Фичи построены для {symbol}")

print("🎯 Фичи построены!")
