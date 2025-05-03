from binance import Client
import pandas as pd
import os

API_KEY = 'QCI76yYs5jbuYqS4geSkEZHhkPJq0QZCOz1pXGIEdIOvfN36RLrkbaaa41OI983T'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCpVLgxywR60Lz9lWDu7votvjLVgwinY6c5wydupOnVRV'

client = Client(API_KEY, API_SECRET)

intervals = ["1m", "5m", "15m", "30m", "1h"]

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

os.makedirs("datasets_full", exist_ok=True)

for symbol in symbols:
    for interval in intervals:
        print(f"Скачиваю {symbol} на таймфрейме {interval}...")
        try:
            klines = client.get_historical_klines(symbol, interval, "60 days ago UTC")
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

            os.makedirs(f"datasets_full/{symbol}", exist_ok=True)
            df.to_csv(f"datasets_full/{symbol}/{symbol}_{interval}.csv")

            print(f"✅ Скачано {symbol} {interval}")

        except Exception as e:
            print(f"⚠️ Ошибка для {symbol} {interval}: {e}")

print("🎯 ВСЯ история скачана!")
