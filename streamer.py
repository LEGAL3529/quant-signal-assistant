import time
from binance import Client
import numpy as np
import pickle
import datetime
import json
import os

# Твои ключи Binance
API_KEY = 'QCI76yYs5jbuYqS4geSkEZHhkPJq0QZiiiiiiiiiiiiiiiiiiiiiiiiiii'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCpVLgxywRiiiiiiiiiiiiiiiiiiiiiiiiii'

client = Client(API_KEY, API_SECRET)

# Загружаем модель
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

# Список пар для мониторинга
symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT"
]

# Получение последних цен
def get_latest_prices(symbol, limit=5):
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=limit)
    closes = [float(kline[4]) for kline in klines]
    return closes

# Логирование сигналов
def log_signal(symbol, prices, signal):
    timestamp = datetime.datetime.utcnow().isoformat()
    log = {
        "timestamp": timestamp,
        "symbol": symbol,
        "prices": prices,
        "signal": signal
    }
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/signals.log", "a") as f:
        f.write(json.dumps(log) + "\n")

# Основной поток
def main_loop(limit=5, interval_sec=60):
    print("🚀 Запуск мульти-потока сигналов...")
    while True:
        for symbol in symbols:
            try:
                prices = get_latest_prices(symbol, limit)
                if len(prices) < limit:
                    print(f"⚠️ Недостаточно данных для {symbol}.")
                    continue

                X = np.array(prices).reshape(1, -1)
                prediction = model.predict(X)[0]
                label = "BUY" if prediction == 1 else "SELL"

                print(f"[{datetime.datetime.utcnow().isoformat()}] {symbol}: {label} — {prices}")

                log_signal(symbol, prices, label)

            except Exception as e:
                print(f"⚠️ Ошибка при обработке {symbol}: {e}")

        time.sleep(interval_sec)

if __name__ == "__main__":
    main_loop()
