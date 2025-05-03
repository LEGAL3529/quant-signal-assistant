import pandas as pd
import xgboost as xgb
import pickle
import os

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

X_total = []
y_total = []

for symbol in symbols:
    df = pd.read_csv(f"datasets/{symbol}_features.csv", index_col=0, parse_dates=True)
    features = df[["return", "volatility", "sma_5", "sma_20", "sma_ratio"]]
    target = df["target"]

    X_total.append(features)
    y_total.append(target)

X = pd.concat(X_total)
y = pd.concat(y_total)

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)

os.makedirs("models", exist_ok=True)
with open("models/signal_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Реальная модель обучена и сохранена!")
