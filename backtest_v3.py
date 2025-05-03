import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

# Загружаем модель
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

results = []

for symbol in symbols:
    df = pd.read_csv(f"datasets/{symbol}_features_v3.csv", index_col=0, parse_dates=True)

    X = df[[
        "return", "volatility", "sma_5", "sma_20", "sma_ratio",
        "ema_5", "ema_20", "rsi_14", "macd", "atr_14", "stoch_k", "stoch_d",
        "bb_width", "obv", "momentum", "cci", "volume_change"
    ]]
    y_true = df["target"]

    preds = model.predict(X)

    df["prediction"] = preds

    # Стратегия: +1 если угадали рост, -1 если не угадали
    df["strategy_return"] = np.where(df["prediction"] == df["target"], df["return"], -df["return"])

    df["cumulative_return"] = (1 + df["strategy_return"]).cumprod()

    results.append(df["cumulative_return"])

    print(f"✅ Бэктест V3 для {symbol}:")
    print(f"  Winrate: {np.mean(df['prediction'] == df['target']):.2f}")
    print(f"  Final return: {df['cumulative_return'].iloc[-1]:.2f}")

# Визуализация
for res, symbol in zip(results, symbols):
    plt.plot(res, label=symbol)

plt.legend()
plt.title("Equity Curve (Backtest V3)")
plt.grid()
plt.show()
