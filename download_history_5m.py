from binance import Client
import pandas as pd
import os

API_KEY = 'QCI76yYs5jbuYqS4geSkEZHhkPJq0QZCOz1pXGIEdIOvfN36Rooooooooooooooo'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCpVLgxywR60Lz9lWDu7votvjLVgwkkkkkkkkkkkkkkk'

client = Client(API_KEY, API_SECRET)

def download_klines(symbol="BTCUSDT", interval="5m", limit=2000):
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

os.makedirs("datasets_5m", exist_ok=True)

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

for symbol in symbols:
    df = download_klines(symbol, limit=3000)
    df.to_csv(f"datasets_5m/{symbol}_history_5m.csv")
    print(f"✅ Скачано для {symbol} (5m таймфрейм)")

print("🎯 Исторические данные 5m собраны!")
