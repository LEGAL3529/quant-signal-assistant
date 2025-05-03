import time
from binance import Client
import numpy as np
import pandas as pd
import ta
import pickle
import os
from sklearn.preprocessing import StandardScaler

# Настоящие ключи Binance
API_KEY = 'QCI76yYs5jbuYqS4geSkEZHhkPJq0QZCOz1pXGIEdIOvfN36RLrkbaaa41OI983T'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCpVLgxywR60Lz9lWDu7votvjLVgwinY6c5wydupOnVRV'

client = Client(API_KEY, API_SECRET)

# Загрузка модели
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

# Функция получения последних цен
def get_latest_prices(symbol, interval="1m", limit=10):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

def get_features(symbol):
    try:
        df_1m = get_latest_prices(symbol, interval="1m", limit=20)
        df_5m = get_latest_prices(symbol, interval="5m", limit=20)

        # 1m фичи
        df_1m["return_1m"] = df_1m["close"].pct_change()
        df_1m["volatility_1m"] = df_1m["return_1m"].rolling(window=10).std()
        df_1m["ema_5_1m"] = df_1m["close"].ewm(span=5).mean()
        df_1m["ema_20_1m"] = df_1m["close"].ewm(span=20).mean()
        df_1m["rsi_14_1m"] = ta.momentum.rsi(df_1m["close"], window=14)

        # 5m фичи
        df_5m["return_5m"] = df_5m["close"].pct_change()
        df_5m["volatility_5m"] = df_5m["return_5m"].rolling(window=10).std()
        df_5m["ema_5_5m"] = df_5m["close"].ewm(span=5).mean()
        df_5m["ema_20_5m"] = df_5m["close"].ewm(span=20).mean()
        df_5m["rsi_14_5m"] = ta.momentum.rsi(df_5m["close"], window=14)

        df = df_1m.join(df_5m, how="left", rsuffix="_5m")
        df.dropna(inplace=True)

        X_live = df[[
            "return_1m", "volatility_1m", "ema_5_1m", "ema_20_1m", "rsi_14_1m",
            "return_5m", "volatility_5m", "ema_5_5m", "ema_20_5m", "rsi_14_5m"
        ]].iloc[-1:]

        return X_live
    except Exception as e:
        print(f"⚠️ Ошибка при сборе данных для {symbol}: {e}")
        return None

print("🚀 Старт реального потока...")

while True:
    for symbol in symbols:
        X_live = get_features(symbol)

        if X_live is not None:
            y_pred = model.predict(X_live)[0]
            y_proba = model.predict_proba(X_live)[0][1]

            if y_pred == 1 and y_proba > 0.6:  # только уверенные сигналы
                print(f"✅ [{symbol}] BUY signal ({y_proba:.2f} confidence)")
            elif y_pred == 0 and y_proba > 0.6:
                print(f"✅ [{symbol}] SELL signal ({(1 - y_proba):.2f} confidence)")

    time.sleep(60)  # ждать 1 минуту перед новым прогнозом
