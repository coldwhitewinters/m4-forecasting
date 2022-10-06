from pathlib import Path


def create_dir(path):
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
    return path


def get_ts(df, name, index="t"):
    y = df.loc[df.name == name].set_index(index)["y"]
    return y
