import pandas as pd
import xgboost as xgb
import pickle
import os
from sklearn.model_selection import train_test_split

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

X_total = []
y_total = []

for symbol in symbols:
    df = pd.read_csv(f"datasets/{symbol}_features_v2.csv", index_col=0, parse_dates=True)

    features = df[[
        "return", "volatility", "sma_5", "sma_20", "sma_ratio",
        "ema_5", "ema_20", "rsi_14", "macd", "volume_change"
    ]]
    target = df["target"]

    X_total.append(features)
    y_total.append(target)

X = pd.concat(X_total)
y = pd.concat(y_total)

# Делим на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Обучаем XGBoost
model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# Сохраняем
os.makedirs("models", exist_ok=True)
with open("models/signal_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Улучшенная модель обучена и сохранена!")
