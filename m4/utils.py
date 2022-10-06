from pathlib import Path
import pandas as pd
from m4.config import DATA_DIR


def create_dir(path):
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
    return path


def load_data(filename, parse_dates=True):
    print(DATA_DIR / f"processed/{filename}")
    df = pd.read_csv(DATA_DIR / f"processed/{filename}", dtype={"category": "category"})
    if parse_dates:
        df["date"] = pd.to_datetime(df["date"])
    return df


def get_ts(df, name, index="t"):
    y = df.loc[df.name == name].set_index(index)["y"]
    return y
