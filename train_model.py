import xgboost as xgb
import pandas as pd
import numpy as np
import pickle

# Создаём фейковый набор данных (10 000 строк)
np.random.seed(42)
X = np.random.randn(10000, 5)  # 5 фичей
y = np.where(np.mean(X, axis=1) > 0, 1, 0)  # 1 = BUY, 0 = SELL

df = pd.DataFrame(X, columns=[f"f{i}" for i in range(5)])
df["target"] = y

# Обучаем модель
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(df.drop("target", axis=1), df["target"])

# Сохраняем модель
with open("models/signal_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Модель обучена и сохранена.")
