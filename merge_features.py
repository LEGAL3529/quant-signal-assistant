import pandas as pd
import os
import glob

output_path = "datasets/features.csv"
feature_files = glob.glob("datasets/*_features.csv")

all_df = []

for file in feature_files:
    symbol = os.path.basename(file).split("_")[0]
    df = pd.read_csv(file)
    df["symbol"] = symbol
    all_df.append(df)

merged = pd.concat(all_df, ignore_index=True)
merged.to_csv(output_path, index=False)

print(f"✅ Saved merged features to {output_path}")

