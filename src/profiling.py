import pandas as pd
from pathlib import Path

DATA_PATH = Path("../data")

files = [
    "lead_log.csv",
    "paid_transactions.csv",
    "referral_rewards.csv",
    "user_logs.csv",
    "user_referral_logs.csv",
    "user_referral_statuses.csv",
    "user_referrals.csv",
]

profiles = []

for file in files:
    df = pd.read_csv(DATA_PATH / file)

    for col in df.columns:
        profiles.append({
            "table": file,
            "column": col,
            "dtype": str(df[col].dtype),
            "null_count": df[col].isna().sum(),
            "distinct_count": df[col].nunique(dropna=True)
        })

profile_df = pd.DataFrame(profiles)
profile_df.to_csv("../profiling_report.csv", index=False)

print("✔ Profiling Complete → profiling_report.csv")
