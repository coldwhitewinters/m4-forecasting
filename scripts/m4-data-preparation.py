import pandas as pd
from pathlib import Path

ROOT = Path("C:/Users/rep2rng/Desktop/home/projects/m4-forecasting")
DATA_DIR = ROOT / "data"
DATASETS = [
    'Daily-test.csv',
    'Daily-train.csv',
    'Hourly-test.csv',
    'Hourly-train.csv',
    'Monthly-test.csv',
    'Monthly-train.csv',
    'Quarterly-test.csv',
    'Quarterly-train.csv',
    'Weekly-test.csv',
    'Weekly-train.csv',
    'Yearly-test.csv',
    'Yearly-train.csv'
]


def create_dir(path):
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
    return path


def remove_trailing_nan(df):
    df = df.set_index("t")
    df = df.loc[:df.y.last_valid_index()].reset_index()
    return df


def add_date_col(df):
    df = df.copy()
    start = df["StartingDate"].iloc[0]
    periods = len(df)
    dates = pd.date_range(start=start, periods=periods)
    df["date"] = dates
    return df


def prepare_data(df, filepath):
    df = df.copy()
    df.columns = pd.Index(["name"] + list(range(df.shape[1] - 1)))
    df = pd.melt(df, id_vars=["name"], value_name="y", var_name="t")
    df["t"] = pd.to_numeric(df["t"])
    df = df.groupby("name").apply(remove_trailing_nan).reset_index(drop=True)
    df = df.merge(m4_info, left_on="name", right_on="M4id")
    df = df.groupby("name").apply(add_date_col)
    df = df.drop(columns=["Frequency", "Horizon", "SP", "M4id", "StartingDate"])
    df = df[["name", "date", "t", "y", "category"]]
    df.to_csv(filepath, index=False)
    print(f"Data written to {filepath}")


if __name__ == "__main__":
    m4_info = pd.read_csv(DATA_DIR / "m4_info.csv")
    processed_data_dir = create_dir(DATA_DIR / "processed")
    for file in DATASETS:
        print(f"Processing {file}")
        df = pd.read_csv(DATA_DIR / file)
        prepare_data(df, processed_data_dir / file)
