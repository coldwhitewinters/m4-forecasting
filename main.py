import pandas as pd

from m4.preprocessing import prepare_data
from m4.utils import create_dir
from m4.config import DATA_DIR, BASE_DATA_DIR, DATASETS


if __name__ == "__main__":
    create_dir(BASE_DATA_DIR)
    for file in DATASETS:
        print(f"Processing {file}")
        df = pd.read_csv(DATA_DIR / file)
        prepare_data(df, BASE_DATA_DIR / file)
