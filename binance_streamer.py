import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from binance import Client
from strategies.ema_rsi_supertrend import apply_strategy

load_dotenv()

API_KEY = os.getenv("QCI76yYs5jbuYqS4geSkEZHhkPJq0QZCOz1pXGIEdIOvfN36Rtyyyyyyyyyyyyyy")
API_SECRET = os.getenv("EpMK5GTSHJxMFf42IhzGCpVLgxywR60Lz9lWDu7votvjLVgwinY6c5pppppppppp")
TELEGRAM_TOKEN = os.getenv("7947328586:AAGhTyJ8bSMU0BrfcXrIPx9SFocZkkkkkkk")
TELEGRAM_CHAT_ID = os.getenv("587kkkkkkk")

client = Client(API_KEY, API_SECRET)

def get_top_symbols(limit=100):
    try:
        tickers = client.get_ticker()
        usdt_pairs = [
            t for t in tickers 
            if t['symbol'].endswith('USDT') 
            and not t['symbol'].endswith('BUSD') 
            and not any(x in t['symbol'] for x in ['UP', 'DOWN', 'LEVER', '1000', 'BULL', 'BEAR'])
        ]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:limit]]
    except Exception as e:
        print(f"[SYMBOL ERROR] {e}")
        return []

def get_ohlcv(symbol):
    try:
        klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=100)
        df = pd.DataFrame(klines, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "num_trades", "taker_buy_vol", "taker_buy_qav", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        return df
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")
        return None

def send_telegram_signal(symbol, signal):
    msg = f"📡 Signal on <b>{symbol}</b>: <b>{signal.upper()}</b>"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=data)
        print(f"[TG OK] Sent {symbol} - {signal.upper()} | Status: {response.status_code}")
        if response.status_code != 200:
            print(f"[TG ERROR] Response: {response.text}")
    except Exception as e:
        print(f"[TG EXCEPTION] {e}")

def stream_signals():
    symbols = get_top_symbols()
    print(f"✅ Tracking {len(symbols)} top symbols")

    while True:
        try:
            for symbol in symbols:
                print(f"🔍 Checking {symbol}")
                df = get_ohlcv(symbol)
                if df is None or len(df) < 20:
                    continue

                signal = apply_strategy(df)
                if signal:
                    print(f"[{symbol}] ✅ SIGNAL: {signal.upper()}")
                    send_telegram_signal(symbol, signal)
                else:
                    print(f"[{symbol}] ❌ No signal")
        except Exception as e:
            print(f"[LOOP ERROR] {e}")

        time.sleep(60)

if __name__ == "__main__":
    print("🚀 Starting Binance Streamer...")
    stream_signals()
