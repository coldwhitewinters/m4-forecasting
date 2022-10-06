import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter

tidyverse = importr("tidyverse")
fable = importr("fable")
feasts = importr("feasts")
lubridate = importr("lubridate")


def pandas_to_r_df(df):
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_df = ro.conversion.py2rpy(df)
    return r_df


def r_to_pandas_df(r_df):
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(r_df)
    return df


def features_feasts(df):
    ro.r(
        """
        features_feasts <- function(df) {
            tsbl <- df %>%
            select(-category) %>%
            mutate(date = as_date(date)) %>%
            as_tsibble(
                key = name,
                index = date
            )

            tsbl_features <- tsbl %>%
                features(
                    y,
                    features = feature_set(pkgs = "feasts")
                )

            return(tsbl_features)
        }
        """
    )

    r_df = pandas_to_r_df(df)
    r_features = ro.r["features_feasts"](r_df)
    features = r_to_pandas_df(r_features)
    return features
