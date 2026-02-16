import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path("../data")
OUTPUT_PATH = Path("../output")

OUTPUT_PATH.mkdir(exist_ok=True)

# -------------------
# LOAD DATA
# -------------------
lead_logs = pd.read_csv(DATA_PATH / "lead_log.csv")
paid_tx = pd.read_csv(DATA_PATH / "paid_transactions.csv")
rewards = pd.read_csv(DATA_PATH / "referral_rewards.csv")
user_logs = pd.read_csv(DATA_PATH / "user_logs.csv")
ref_logs = pd.read_csv(DATA_PATH / "user_referral_logs.csv")
statuses = pd.read_csv(DATA_PATH / "user_referral_statuses.csv")
referrals = pd.read_csv(DATA_PATH / "user_referrals.csv")

# -------------------
# FIX DATETIME
# -------------------
lead_logs['created_at'] = pd.to_datetime(lead_logs['created_at'])
paid_tx['transaction_at'] = pd.to_datetime(paid_tx['transaction_at'])
user_logs['membership_expired_date'] = pd.to_datetime(user_logs['membership_expired_date'])
ref_logs['created_at'] = pd.to_datetime(ref_logs['created_at'])
referrals['referral_at'] = pd.to_datetime(referrals['referral_at'])
referrals['updated_at'] = pd.to_datetime(referrals['updated_at'])

# -------------------
# CLEAN REWARD VALUE ("30 days" → 30)
# -------------------
rewards['reward_value'] = (
    rewards['reward_value']
    .str.extract(r'(\d+)')
    .astype(float)
)

# -------------------
# REMOVE NULL KEYS
# -------------------
referrals = referrals.dropna(subset=['referral_id', 'referrer_id'])

# -------------------
# STRING NORMALIZATION (Initcap)
# -------------------
referrals['referral_source'] = referrals['referral_source'].str.title()
statuses['description'] = statuses['description'].str.title()
paid_tx['transaction_status'] = paid_tx['transaction_status'].str.title()
paid_tx['transaction_type'] = paid_tx['transaction_type'].str.title()

# -------------------
# JOINS
# -------------------

# Join referral status
df = referrals.merge(
    statuses[['id', 'description']],
    left_on='user_referral_status_id',
    right_on='id',
    how='left'
).rename(columns={'description': 'referral_status'})

# Join rewards
df = df.merge(
    rewards[['id', 'reward_value']],
    left_on='referral_reward_id',
    right_on='id',
    how='left'
)

# Join transactions
df = df.merge(paid_tx, on='transaction_id', how='left')

# Join referrer details
df = df.merge(
    user_logs[['user_id', 'name', 'phone_number', 'homeclub',
               'membership_expired_date', 'is_deleted']],
    left_on='referrer_id',
    right_on='user_id',
    how='left'
).rename(columns={
    'name': 'referrer_name',
    'phone_number': 'referrer_phone_number',
    'homeclub': 'referrer_homeclub'
})

# Join referral logs (reward granted)
df = df.merge(
    ref_logs[['user_referral_id', 'created_at', 'is_reward_granted']],
    left_on='referral_id',
    right_on='user_referral_id',
    how='left'
)

df = df.rename(columns={'created_at': 'reward_granted_at'})

# -------------------
# REMOVE TIMEZONE AWARENESS (safe comparisons)
# -------------------
for col in ['transaction_at', 'referral_at', 'membership_expired_date']:
    df[col] = pd.to_datetime(df[col], errors='coerce').dt.tz_localize(None)

# -------------------
# BUSINESS LOGIC FLAGS
# -------------------

df['transaction_after_referral'] = df['transaction_at'] > df['referral_at']

df['same_month'] = (
    df['transaction_at'].dt.to_period('M') ==
    df['referral_at'].dt.to_period('M')
)

df['membership_valid'] = (
    df['membership_expired_date'] >= df['transaction_at']
)

# -------------------
# VALID CONDITIONS
# -------------------

valid_1 = (
    (df['reward_value'] > 0) &
    (df['referral_status'] == 'Berhasil') &
    (df['transaction_id'].notna()) &
    (df['transaction_status'] == 'Paid') &
    (df['transaction_type'] == 'New') &
    (df['transaction_after_referral']) &
    (df['same_month']) &
    (df['membership_valid']) &
    (~df['is_deleted'].fillna(True).astype(bool)) &
    (df['is_reward_granted'] == True)
)

valid_2 = (
    df['referral_status'].isin(['Menunggu', 'Tidak Berhasil']) &
    df['reward_value'].isna()
)

df['is_business_logic_valid'] = valid_1 | valid_2

# -------------------
# FINAL REPORT
# -------------------
report = df[[
    'referral_id',
    'referral_source',
    'referral_at',
    'referrer_id',
    'referrer_name',
    'referrer_phone_number',
    'referrer_homeclub',
    'referee_id',
    'referee_name',
    'referee_phone',
    'referral_status',
    'reward_value',
    'transaction_id',
    'transaction_status',
    'transaction_at',
    'transaction_location',
    'transaction_type',
    'updated_at',
    'reward_granted_at',
    'is_business_logic_valid'
]].drop_duplicates()

# -------------------
# SAVE OUTPUT
# -------------------
report.to_csv(OUTPUT_PATH / "referral_validation_report.csv", index=False)

print("✔ Pipeline Complete")
print("Final Rows:", report.shape)
