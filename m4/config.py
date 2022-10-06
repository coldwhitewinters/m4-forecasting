from pathlib import Path


# Config
# -----------------------------------------------------------------------------

root = "/home/ec2-user/m4-forecasting"
datasets = [
    'Test/Hourly-test.csv',
    'Test/Daily-test.csv',
    'Test/Weekly-test.csv',
    'Test/Monthly-test.csv',
    'Test/Quarterly-test.csv',
    'Test/Yearly-test.csv',
    'Train/Hourly-train.csv',
    'Train/Daily-train.csv',
    'Train/Weekly-train.csv',
    'Train/Monthly-train.csv',
    'Train/Quarterly-train.csv',
    'Train/Yearly-train.csv',
]
settings = {
    "unzip": True,
    "prepare_data": True,
}

# -----------------------------------------------------------------------------

root = Path(root)
paths = {
    "root": root,
    "data_dir": root / "data",
    "data_dir_raw": root / "data/raw",
    "data_dir_processed": root / "data/processed",
    "data_dir_base": root / "data/processed/base",
    "data_dir_features": root / "data/processed/features",
}
