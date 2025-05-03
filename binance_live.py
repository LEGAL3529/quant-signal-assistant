from binance import Client
import numpy as np
import pickle

# Подключение через твои ключи
API_KEY = 'QCI76yYs5jbuYqS4geSkEZHhkPJq0QZCOz1pXGIEdIOvfN36RLrkbaaa41OI983T'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCpVLgxywR60Lz9lWDu7votvjLVgwinY6c5wydupOnVRV'

client = Client(API_KEY, API_SECRET)

# Загружаем модель
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

# Функция получить последние цены
def get_latest_prices(symbol="BTCUSDT", limit=5):
    klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=limit)
    closes = [float(kline[4]) for kline in klines]  # Цена закрытия каждой свечи
    return closes

# Получаем данные
prices = get_latest_prices()

# Подаём в модель
X = np.array(prices).reshape(1, -1)
prediction = model.predict(X)[0]
label = "BUY" if prediction == 1 else "SELL"

print(f"🧠 Реальный сигнал для {prices}: {label}")
