import pandas as pd
from pathlib import Path
from zipfile import ZipFile

from m4.preprocessing import prepare_data
from m4.utils import create_dir
from m4.config import paths, datasets, settings


if __name__ == "__main__":

    if settings["unzip"]:
        with ZipFile(paths["data_dir"] / "m4-forecasting.zip", 'r') as f:
            f.extractall(paths["data_dir_raw"])

    if settings["prepare_data"]:
        create_dir(paths["data_dir_base"])
        for fp in datasets:
            print(f"Processing {fp}")
            fp = Path(fp)
            df = pd.read_csv(paths["data_dir_raw"] / fp)
            prepare_data(df, paths["data_dir_base"] / fp.name.lower())
