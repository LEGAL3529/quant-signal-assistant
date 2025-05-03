import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report
import joblib
import json
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def load_and_merge_data():
    trades = pd.read_csv("trades.csv")
    features = pd.read_csv("datasets/features.csv")

    trades["timestamp"] = pd.to_datetime(trades["timestamp"]).dt.floor("min")
    features["timestamp"] = pd.to_datetime(features["timestamp"]).dt.floor("min")

    df = pd.merge(trades, features, on=["timestamp", "symbol"], how="inner")
    return df

def build_target(df):
    feedback_cols = ["feedback_15m", "feedback_1h", "feedback_4h"]
    weights = [0.2, 0.5, 0.3]

    for col in feedback_cols:
        if col not in df.columns:
            df[col] = np.nan

    df["meta_feedback"] = df[feedback_cols].dot(weights)
    df = df.dropna(subset=["meta_feedback"])
    df["target"] = (df["meta_feedback"] >= 0.5).astype(int)
    return df

def train_agentic_model():
    df = load_and_merge_data()
    df = build_target(df)

    if len(df) < 10:
        print(f"❌ Недостаточно данных после объединения: {len(df)} строк. Ждём больше трейдов.")
        return

    feature_cols = [col for col in df.columns if col not in [
        "timestamp", "symbol", "pnl", "meta_feedback", "target"
    ] and not col.startswith("feedback")]

    X = df[feature_cols].fillna(0)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    lgb = LGBMClassifier(n_estimators=150)
    cat = CatBoostClassifier(verbose=0, iterations=150)
    logreg = LogisticRegressionCV(cv=5, max_iter=500)

    ensemble = VotingClassifier(estimators=[
        ("lgb", lgb),
        ("cat", cat),
        ("logreg", logreg)
    ], voting="soft")

    calibrated = CalibratedClassifierCV(ensemble, method="isotonic", cv=3)
    calibrated.fit(X_train, y_train)

    y_pred = calibrated.predict(X_test)
    y_prob = calibrated.predict_proba(X_test)[:, 1]

    print("✅ Classification Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(calibrated, "model_agentic.pkl")

    importance = dict(zip(X.columns, lgb.feature_importances_))
    importance = dict(sorted(importance.items(), key=lambda x: -x[1]))
    with open("feature_importance.json", "w") as f:
        json.dump(importance, f, indent=2)

    print("✅ Model saved as model_agentic.pkl")
    print("✅ Feature importance saved as feature_importance.json")

if __name__ == "__main__":
    train_agentic_model()
