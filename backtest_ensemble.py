import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Загружаем модели
with open("models/signal_model_ensemble.pkl", "rb") as f:
    model_xgb, model_lgb, model_cat = pickle.load(f)

# Данные
symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

# Собираем все данные
X_total = []
y_total = []
returns_total = []

for symbol in symbols:
    try:
        df = pd.read_csv(f"datasets_features_multi_tf/{symbol}_features_multi_tf.csv", index_col=0, parse_dates=True)

        features = df[[
            "return_1m", "volatility_1m", "ema_5_1m", "ema_20_1m", "rsi_14_1m",
            "return_5m", "volatility_5m", "ema_5_5m", "ema_20_5m", "rsi_14_5m",
            "return_15m", "volatility_15m", "ema_5_15m", "ema_20_15m", "rsi_14_15m",
            "return_30m", "volatility_30m", "ema_5_30m", "ema_20_30m", "rsi_14_30m",
            "return_1h", "volatility_1h", "ema_5_1h", "ema_20_1h", "rsi_14_1h"
        ]]
        target = df["target"]
        returns = df["return_1m"]

        X_total.append(features)
        y_total.append(target)
        returns_total.append(returns)

    except Exception as e:
        print(f"⚠️ Ошибка обработки {symbol}: {e}")
        continue

X = pd.concat(X_total)
y = pd.concat(y_total)
returns = pd.concat(returns_total)

# Делим на train/test
split_index = int(0.7 * len(X))
X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]
returns_test = returns.iloc[split_index:]

# Предсказания ансамбля
proba_xgb = model_xgb.predict_proba(X_test)[:, 1]
proba_lgb = model_lgb.predict_proba(X_test)[:, 1]
proba_cat = model_cat.predict_proba(X_test)[:, 1]

proba_ensemble = (proba_xgb + proba_lgb + proba_cat) / 3
y_pred = (proba_ensemble > 0.5).astype(int)

# Стратегия: если правильно предсказали — зарабатываем ретурн, иначе -ретурн
strategy_returns = np.where(y_pred == y_test, returns_test, -returns_test)

# Учитываем комиссию (примерно 0.075% на вход и выход)
commission = 0.0015  # вход + выход = 0.075% + 0.075%
strategy_returns = strategy_returns - commission

# Строим cumulative return
equity_curve = pd.Series((1 + strategy_returns).cumprod())

# Метрики
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

# Просадка
drawdown = (equity_curve.cummax() - equity_curve) / equity_curve.cummax()
max_drawdown = drawdown.max()

# Sharpe Ratio
sharpe_ratio = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252*24*60)  # пересчёт на годовые

# Вывод
print("🎯 Улучшенный Бэктест:")
print(f"✅ Accuracy: {accuracy:.4f}")
print(f"✅ Precision: {precision:.4f}")
print(f"✅ Recall: {recall:.4f}")
print(f"✅ F1 Score: {f1:.4f}")
print(f"✅ Максимальная просадка: {max_drawdown:.4f}")
print(f"✅ Sharpe Ratio: {sharpe_ratio:.2f}")

# График
plt.figure(figsize=(14,7))
plt.plot(equity_curve)
plt.title("Equity Curve (Ensemble)")
plt.grid()
plt.show()
