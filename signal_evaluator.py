import pandas as pd
import json

def evaluate_signals(trades_path="trades.csv", features_path="datasets/features.csv", output_path="signal_evaluation.json"):
    try:
        trades = pd.read_csv(trades_path)
        features = pd.read_csv(features_path)

        if "symbol" not in trades.columns or "timestamp" not in trades.columns:
            raise ValueError("Missing 'symbol' or 'timestamp' in trades.csv")

        if "entry_price" not in trades.columns:
            raise ValueError("Missing 'entry_price' in trades.csv")

        trades["timestamp"] = pd.to_datetime(trades["timestamp"])
        features["timestamp"] = pd.to_datetime(features["timestamp"])

        # Соединяем по timestamp + symbol
        df = pd.merge(trades, features, on=["timestamp", "symbol"], how="inner")

        results = {}

        # Какие feedback_* есть
        feedback_cols = [col for col in df.columns if col.startswith("feedback_")]

        # Анализ по каждой фиче
        feature_cols = [col for col in features.columns if col not in ["timestamp", "symbol"]]

        for feature in feature_cols:
            stats = {}
            for fb_col in feedback_cols:
                valid = df[[feature, fb_col]].dropna()
                if len(valid) == 0:
                    continue

                grouped = valid.groupby(pd.cut(valid[feature], bins=5))
                feature_stats = []
                for bin_range, group in grouped:
                    winrate = group[fb_col].mean()
                    count = len(group)
                    feature_stats.append({
                        "range": str(bin_range),
                        "winrate": round(winrate * 100, 2),
                        "count": count
                    })
                stats[fb_col] = feature_stats
            results[feature] = stats

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"✅ Saved evaluation to {output_path}")
    except Exception as e:
        print(f"❌ Evaluation error: {e}")

if __name__ == "__main__":
    evaluate_signals()
