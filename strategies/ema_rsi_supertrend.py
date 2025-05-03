import numpy as np
import pandas as pd

def supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = df['high'].rolling(period).max() - df['low'].rolling(period).min()
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    return upperband, lowerband

def apply_strategy(df):
    df['ema'] = df['close'].ewm(span=20).mean()
    df['rsi'] = compute_rsi(df['close'])

    upper, lower = supertrend(df)
    df['supertrend_long'] = df['close'] > upper
    df['supertrend_short'] = df['close'] < lower

    signal = None
    if (
        df['close'].iloc[-1] > df['ema'].iloc[-1] and
        df['rsi'].iloc[-1] < 70 and
        df['supertrend_long'].iloc[-1]
    ):
        signal = "buy"
    elif (
        df['close'].iloc[-1] < df['ema'].iloc[-1] and
        df['rsi'].iloc[-1] > 30 and
        df['supertrend_short'].iloc[-1]
    ):
        signal = "sell"

    return signal

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
