import pandas as pd
import ta
import os

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

intervals = ["1m", "5m", "15m", "30m", "1h"]

os.makedirs("datasets_features_multi_tf", exist_ok=True)

for symbol in symbols:
    try:
        # Загружаем все таймфреймы
        dfs = {}
        for interval in intervals:
            df = pd.read_csv(f"datasets_full/{symbol}/{symbol}_{interval}.csv", index_col=0, parse_dates=True)
            dfs[interval] = df

        # Обрабатываем 1m как базовый
        df_base = dfs["1m"]

        # Строим фичи для 1m
        df_base["return_1m"] = df_base["close"].pct_change()
        df_base["volatility_1m"] = df_base["return_1m"].rolling(window=10).std()
        df_base["ema_5_1m"] = ta.trend.ema_indicator(df_base["close"], window=5)
        df_base["ema_20_1m"] = ta.trend.ema_indicator(df_base["close"], window=20)
        df_base["rsi_14_1m"] = ta.momentum.rsi(df_base["close"], window=14)

        # Добавляем фичи с других таймфреймов (через join)
        for interval in ["5m", "15m", "30m", "1h"]:
            df = dfs[interval]
            df_resampled = df.resample('1T').ffill()  # подгоняем под 1 минуту
            df_resampled[f"return_{interval}"] = df_resampled["close"].pct_change()
            df_resampled[f"volatility_{interval}"] = df_resampled[f"return_{interval}"].rolling(window=10).std()
            df_resampled[f"ema_5_{interval}"] = ta.trend.ema_indicator(df_resampled["close"], window=5)
            df_resampled[f"ema_20_{interval}"] = ta.trend.ema_indicator(df_resampled["close"], window=20)
            df_resampled[f"rsi_14_{interval}"] = ta.momentum.rsi(df_resampled["close"], window=14)

            # Только нужные колонки
            df_features = df_resampled[[
                f"return_{interval}", f"volatility_{interval}", 
                f"ema_5_{interval}", f"ema_20_{interval}", f"rsi_14_{interval}"
            ]]

            # Джойним к базе
            df_base = df_base.join(df_features, how="left")

        # Строим таргет: через 5 минут рост более 0.2%
        future_return = (df_base["close"].shift(-5) - df_base["close"]) / df_base["close"]
        df_base["target"] = (future_return > 0.002).astype(int)

        df_base.dropna(inplace=True)

        # Сохраняем
        df_base.to_csv(f"datasets_features_multi_tf/{symbol}_features_multi_tf.csv")
        print(f"✅ Построены мульти-таймфрейм фичи для {symbol}")

    except Exception as e:
        print(f"⚠️ Ошибка обработки {symbol}: {e}")

print("🎯 Все мульти-таймфрейм фичи построены!")
