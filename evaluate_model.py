import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", 
    "MATICUSDT", "DOTUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT", "LTCUSDT", "ATOMUSDT",
    "NEARUSDT", "FILUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "SANDUSDT"
]

# Загружаем данные
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

# Загружаем модель
with open("models/signal_model.pkl", "rb") as f:
    model = pickle.load(f)

# Предсказания
y_pred = model.predict(X_test)

# Метрики
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

print("✅ Оценка качества модели:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
