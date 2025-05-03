import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

# Загружаем модель
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

results = []

for symbol in symbols:
    df = pd.read_csv(f"datasets_multi_tf/{symbol}_features_multi_tf.csv", index_col=0, parse_dates=True)

    X = df[[
        "return_1m", "volatility_1m", "ema_5_1m", "ema_20_1m", "rsi_14_1m",
        "return_5m", "volatility_5m", "ema_5_5m", "ema_20_5m", "rsi_14_5m"
    ]]
    y_true = df["target"]

    preds = model.predict(X)

    df["prediction"] = preds

    df["strategy_return"] = np.where(df["prediction"] == df["target"], df["return_1m"], -df["return_1m"])

    df["cumulative_return"] = (1 + df["strategy_return"]).cumprod()

    results.append(df["cumulative_return"])

    print(f"✅ Бэктест Multi-TF для {symbol}:")
    print(f"  Winrate: {np.mean(df['prediction'] == df['target']):.2f}")
    print(f"  Final return: {df['cumulative_return'].iloc[-1]:.2f}")

# График
for res, symbol in zip(results, symbols):
    plt.plot(res, label=symbol)

plt.legend()
plt.title("Equity Curve (Backtest Multi-TF)")
plt.grid()
plt.show()
