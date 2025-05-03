import pandas as pd
import ta  # Technical Analysis library
import os

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

for symbol in symbols:
    df = pd.read_csv(f"datasets/{symbol}_history.csv", index_col=0, parse_dates=True)

    # Строим базовые фичи
    df["return"] = df["close"].pct_change()
    df["volatility"] = df["return"].rolling(window=10).std()
    df["sma_5"] = df["close"].rolling(window=5).mean()
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_ratio"] = df["sma_5"] / df["sma_20"]

    # Новые фичи (через ta)
    df["ema_5"] = ta.trend.ema_indicator(df["close"], window=5)
    df["ema_20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["rsi_14"] = ta.momentum.rsi(df["close"], window=14)
    df["macd"] = ta.trend.macd(df["close"])

    df["volume_change"] = df["volume"].pct_change()

    # Улучшаем таргет:
    # 1 — если цена через 5 минут выросла больше чем на 0.2%
    # 0 — иначе
    future_return = (df["close"].shift(-5) - df["close"]) / df["close"]
    df["target"] = (future_return > 0.002).astype(int)

    df.dropna(inplace=True)

    df.to_csv(f"datasets/{symbol}_features_v2.csv")
    print(f"✅ Улучшенные фичи построены для {symbol}")

print("🎯 Улучшенные фичи построены!")
