import pandas as pd
import ta
import os

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

for symbol in symbols:
    df = pd.read_csv(f"datasets/{symbol}_history.csv", index_col=0, parse_dates=True)

    # Базовые фичи
    df["return"] = df["close"].pct_change()
    df["volatility"] = df["return"].rolling(window=10).std()
    df["sma_5"] = df["close"].rolling(window=5).mean()
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_ratio"] = df["sma_5"] / df["sma_20"]

    # Технические индикаторы
    df["ema_5"] = ta.trend.ema_indicator(df["close"], window=5)
    df["ema_20"] = ta.trend.ema_indicator(df["close"], window=20)
    df["rsi_14"] = ta.momentum.rsi(df["close"], window=14)
    df["macd"] = ta.trend.macd(df["close"])

    df["atr_14"] = ta.volatility.average_true_range(df["high"], df["low"], df["close"], window=14)
    df["stoch_k"] = ta.momentum.stoch(df["high"], df["low"], df["close"], window=14)
    df["stoch_d"] = ta.momentum.stoch_signal(df["high"], df["low"], df["close"], window=14)
    df["bb_width"] = ta.volatility.bollinger_wband(df["close"], window=20)
    df["obv"] = ta.volume.on_balance_volume(df["close"], df["volume"])
    df["momentum"] = ta.momentum.roc(df["close"], window=10)
    df["cci"] = ta.trend.cci(df["high"], df["low"], df["close"], window=20)

    df["volume_change"] = df["volume"].pct_change()

    # Улучшенный таргет:
    future_return = (df["close"].shift(-5) - df["close"]) / df["close"]
    df["target"] = (future_return > 0.002).astype(int)

    df.dropna(inplace=True)

    df.to_csv(f"datasets/{symbol}_features_v3.csv")
    print(f"✅ Построены супер-фичи для {symbol}")

print("🎯 Все супер-фичи построены!")
