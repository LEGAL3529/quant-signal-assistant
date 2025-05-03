import pandas as pd
import pickle
import os
import numpy as np

# Загружаем XGBoost, LightGBM, CatBoost
with open("models/signal_model.pkl", "rb") as f:
    model_xgb = pickle.load(f)

with open("models/signal_model_lgb.pkl", "rb") as f:
    model_lgb = pickle.load(f)

with open("models/signal_model_cat.pkl", "rb") as f:
    model_cat = pickle.load(f)

# Загружаем фичи
symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

X_total = []
y_total = []

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

        X_total.append(features)
        y_total.append(target)

        print(f"✅ Загружены данные для {symbol}")

    except Exception as e:
        print(f"⚠️ Ошибка при обработке {symbol}: {e}")
        continue

X = pd.concat(X_total)
y = pd.concat(y_total)

# Делим по времени
split_index = int(0.7 * len(X))
X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Предсказания трёх моделей
proba_xgb = model_xgb.predict_proba(X_test)[:, 1]
proba_lgb = model_lgb.predict_proba(X_test)[:, 1]
proba_cat = model_cat.predict_proba(X_test)[:, 1]

# Среднее вероятностей
proba_ensemble = (proba_xgb + proba_lgb + proba_cat) / 3

# Прогноз
y_pred = (proba_ensemble > 0.5).astype(int)

# Метрики
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("🎯 Оценка качества АНСАМБЛЯ:")
print(f"✅ Accuracy: {accuracy:.4f}")
print(f"✅ Precision: {precision:.4f}")
print(f"✅ Recall: {recall:.4f}")
print(f"✅ F1 Score: {f1:.4f}")

# Сохраняем вероятности ансамбля для будущего использования
os.makedirs("models", exist_ok=True)
with open("models/signal_model_ensemble.pkl", "wb") as f:
    pickle.dump((model_xgb, model_lgb, model_cat), f)

print("🎯 Ансамбль моделей сохранён!")
