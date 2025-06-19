import time
from binance import Client
import pandas as pd
import ta
import pickle
import numpy as np
import asyncio
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from signal_logger import log_signal

# 🔧 Настройки
API_KEY = 'QCI76yYs5jbuYqS4geSkEiiiiiiiiiiiiiiii'
API_SECRET = 'EpMK5GTSHJxMFf42IhzGCiiiiiiiiiiiii'
TELEGRAM_TOKEN = '7947328586:AAGiiiiiiiiiiiiiiiii'
TELEGRAM_CHAT_ID = '587iiiiiiii4'

client = Client(API_KEY, API_SECRET)
tg_bot = Bot(token=TELEGRAM_TOKEN)

# 📦 Модели
with open("models/signal_model_ensemble.pkl", "rb") as f:
    model_xgb, model_lgb, model_cat = pickle.load(f)

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT",
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

async def send_signal_with_buttons(symbol, signal_type, confidence):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("👍 Вход", callback_data=f"confirm:{symbol}:{signal_type}:{confidence}"),
        InlineKeyboardButton("👎 Пропустить", callback_data=f"skip:{symbol}")
    )
    kb.add(InlineKeyboardButton("📊 Отчёт", callback_data="report"))

    msg = f"📈 [{symbol}] {signal_type} сигнал 🚀\nУверенность: {confidence:.2%}"
    await tg_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, reply_markup=kb)

def get_latest_prices(symbol, interval="1m", limit=20):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    except:
        return pd.DataFrame()

def build_features(symbol):
    try:
        def safe_resample(df):
            return df.resample('1min').ffill() if len(df) > 0 else pd.DataFrame()

        df_1m = get_latest_prices(symbol, "1m")
        df_5m = get_latest_prices(symbol, "5m")
        df_15m = get_latest_prices(symbol, "15m")
        df_30m = get_latest_prices(symbol, "30m")
        df_1h = get_latest_prices(symbol, "1h")

        if len(df_1m) < 15:
            return None

        df = df_1m.copy()
        df["return_1m"] = df["close"].pct_change()
        df["volatility_1m"] = df["return_1m"].rolling(10).std()
        df["ema_5_1m"] = ta.trend.ema_indicator(df["close"], 5)
        df["ema_20_1m"] = ta.trend.ema_indicator(df["close"], 20)
        df["rsi_14_1m"] = ta.momentum.rsi(df["close"], 14)

        for tf, df_tf in zip(["5m", "15m", "30m", "1h"], [df_5m, df_15m, df_30m, df_1h]):
            df_tf = safe_resample(df_tf)
            if df_tf.empty:
                return None
            df[f"return_{tf}"] = df_tf["close"].pct_change()
            df[f"volatility_{tf}"] = df[f"return_{tf}"].rolling(10).std()
            df[f"ema_5_{tf}"] = ta.trend.ema_indicator(df_tf["close"], 5)
            df[f"ema_20_{tf}"] = ta.trend.ema_indicator(df_tf["close"], 20)
            df[f"rsi_14_{tf}"] = ta.momentum.rsi(df_tf["close"], 14)

        df.dropna(inplace=True)
        return df

    except:
        return None

print("🚀 Запуск стриминга сигналов с кнопками...")

while True:
    for symbol in symbols:
        features = build_features(symbol)
        if features is None:
            continue

        X_live = features[[
            "return_1m", "volatility_1m", "ema_5_1m", "ema_20_1m", "rsi_14_1m",
            "return_5m", "volatility_5m", "ema_5_5m", "ema_20_5m", "rsi_14_5m",
            "return_15m", "volatility_15m", "ema_5_15m", "ema_20_15m", "rsi_14_15m",
            "return_30m", "volatility_30m", "ema_5_30m", "ema_20_30m", "rsi_14_30m",
            "return_1h", "volatility_1h", "ema_5_1h", "ema_20_1h", "rsi_14_1h"
        ]].iloc[-1:]

        if X_live.empty:
            continue

        try:
            proba_xgb = model_xgb.predict_proba(X_live)[0][1]
            proba_lgb = model_lgb.predict_proba(X_live)[0][1]
            proba_cat = model_cat.predict_proba(X_live)[0][1]

            proba = (proba_xgb + proba_lgb + proba_cat) / 3

            if proba > 0.6:
                asyncio.run(send_signal_with_buttons(symbol, "BUY", proba))
                log_signal(symbol, "BUY", proba)
                print(f"📈 BUY {symbol} {proba:.2%}")

            elif proba < 0.4:
                asyncio.run(send_signal_with_buttons(symbol, "SELL", 1 - proba))
                log_signal(symbol, "SELL", 1 - proba)
                print(f"📉 SELL {symbol} {1 - proba:.2%}")

        except Exception as e:
            print(f"Ошибка: {e}")

    time.sleep(60)
