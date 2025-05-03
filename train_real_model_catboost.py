import pandas as pd
from catboost import CatBoostClassifier
import pickle
import os

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

# Склеиваем
X = pd.concat(X_total)
y = pd.concat(y_total)

# Делим по времени (70% train, 30% test)
split_index = int(0.7 * len(X))
X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# CatBoost модель
model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.02,
    depth=7,
    loss_function='Logloss',
    verbose=200,
    random_seed=42
)

model.fit(X_train, y_train)

# Сохраняем
os.makedirs("models", exist_ok=True)
with open("models/signal_model_cat.pkl", "wb") as f:
    pickle.dump(model, f)

print("🎯 CatBoost модель обучена и сохранена!")

# Тест
accuracy = model.score(X_test, y_test)
print(f"✅ Accuracy CatBoost на тесте: {accuracy:.4f}")
