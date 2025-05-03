import pandas as pd
import ta
import os

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

for symbol in symbols:
    df_1m = pd.read_csv(f"datasets/{symbol}_history.csv", index_col=0, parse_dates=True)
    df_5m = pd.read_csv(f"datasets_5m/{symbol}_history_5m.csv", index_col=0, parse_dates=True)

    # 1m фичи
    df_1m["return_1m"] = df_1m["close"].pct_change()
    df_1m["volatility_1m"] = df_1m["return_1m"].rolling(window=10).std()
    df_1m["ema_5_1m"] = ta.trend.ema_indicator(df_1m["close"], window=5)
    df_1m["ema_20_1m"] = ta.trend.ema_indicator(df_1m["close"], window=20)
    df_1m["rsi_14_1m"] = ta.momentum.rsi(df_1m["close"], window=14)

    # 5m фичи
    df_5m["return_5m"] = df_5m["close"].pct_change()
    df_5m["volatility_5m"] = df_5m["return_5m"].rolling(window=10).std()
    df_5m["ema_5_5m"] = ta.trend.ema_indicator(df_5m["close"], window=5)
    df_5m["ema_20_5m"] = ta.trend.ema_indicator(df_5m["close"], window=20)
    df_5m["rsi_14_5m"] = ta.momentum.rsi(df_5m["close"], window=14)

    # Объединяем 1m + 5m
    df = df_1m.join(df_5m, how="left", rsuffix="_5m")

    # Целевая переменная (через 5 минут рост больше 0.2%)
    future_return = (df["close"].shift(-5) - df["close"]) / df["close"]
    df["target"] = (future_return > 0.002).astype(int)

    df.dropna(inplace=True)

    os.makedirs("datasets_multi_tf", exist_ok=True)
    df.to_csv(f"datasets_multi_tf/{symbol}_features_multi_tf.csv")
    print(f"✅ Фичи мульти-таймфрейма построены для {symbol}")

print("🎯 Все мульти-таймфрейм фичи построены!")
