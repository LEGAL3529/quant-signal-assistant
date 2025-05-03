import pandas as pd
import xgboost as xgb
import pickle
import os
from sklearn.model_selection import train_test_split

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

X_total = []
y_total = []

for symbol in symbols:
    df = pd.read_csv(f"datasets_multi_tf/{symbol}_features_multi_tf.csv", index_col=0, parse_dates=True)

    features = df[[
        "return_1m", "volatility_1m", "ema_5_1m", "ema_20_1m", "rsi_14_1m",
        "return_5m", "volatility_5m", "ema_5_5m", "ema_20_5m", "rsi_14_5m"
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
    n_estimators=800,
    max_depth=7,
    learning_rate=0.02,
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

print("✅ Мульти-таймфрейм модель обучена и сохранена!")
