import pandas as pd
from m4.config import DATA_DIR


def remove_trailing_nan(df):
    df = df.set_index("t")
    df = df.loc[:df.y.last_valid_index()].reset_index()
    return df


def parse_dates(m4_info):
    dates = []

    match = m4_info.StartingDate.str.fullmatch(r"\d\d-\d\d-\d\d \d\d:\d\d")
    dates.append(pd.to_datetime(m4_info.loc[match, "StartingDate"], format="%d-%m-%y %H:%M"))

    match = m4_info.StartingDate.str.fullmatch(r"\d\d-\d\d-\d\d \d:\d\d")
    dates.append(pd.to_datetime(m4_info.loc[match, "StartingDate"], format="%d-%m-%y %H:%M"))

    match = m4_info.StartingDate.str.fullmatch(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")
    dates.append(pd.to_datetime(m4_info.loc[match, "StartingDate"], format="%Y-%m-%d %H:%M:%S"))

    dates = pd.concat(dates)
    dates[dates.dt.year > 2018] = dates[dates.dt.year > 2018] - pd.offsets.DateOffset(years=100)

    m4_info = m4_info.copy()
    m4_info["StartingDate"] = dates

    return m4_info


def add_date_col(df):
    df = df.copy()
    freq = df["SP"].iloc[0]

    freq_alias = {
        "Yearly": "Y",
        "Quarterly": "Q",
        "Monthly": "MS",
        "Weekly": "W",
        "Daily": "D",
        "Hourly": "H",
    }

    start = df["StartingDate"].iloc[0]
    periods = len(df)
    try:
        dates = pd.date_range(start=start, periods=periods, freq=freq_alias[freq], normalize=True)
    except pd.errors.OutOfBoundsDatetime:
        dates = pd.DatetimeIndex([pd.NaT for _ in range(periods)])
    df["date"] = dates
    return df


def prepare_data(df, filepath):
    m4_info = pd.read_csv(DATA_DIR / "m4_info.csv")
    m4_info = parse_dates(m4_info)

    df.columns = pd.Index(["name"] + list(range(df.shape[1] - 1)))
    df = pd.melt(df, id_vars=["name"], value_name="y", var_name="t")
    df["t"] = pd.to_numeric(df["t"])
    df = df.groupby("name").apply(remove_trailing_nan).reset_index(drop=True)
    df = df.merge(m4_info, left_on="name", right_on="M4id")
    df = df.groupby("name").apply(add_date_col)
    df = df[["name", "date", "t", "y", "category"]]
    df.to_csv(filepath, index=False)
    print(f"Data written to {filepath}")
