library(tidyverse)
library(fpp3)
library(arrow)

daily_train <- read_parquet("../data/processed/daily-train-base.parquet")

daily_train <- daily_train %>% 
  select(-`__index_level_0__`) %>%
  mutate(ds = as_date(ds)) %>%
  as_tsibble(key=id, index=ds)

daily_train_features <- daily_train %>%
  features(y, list(
    feat_acf,
    feat_pacf,
    feat_stl, 
    feat_spectral,
    unitroot_ndiffs,
    unitroot_nsdiffs,
    n_crossing_points, 
    longest_flat_spot,
    var_tiled_mean,
    var_tiled_var
    # shift_level_max,
    # shift_var_max,
    # shift_kl_max,
    # coef_hurst,
    # guerrero,
    )
  )

