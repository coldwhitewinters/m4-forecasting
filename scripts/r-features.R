library(tidyverse)
library(fpp3)

daily_train <- read_csv("./data/processed/daily-train-base.csv")

daily_train <- daily_train %>% 
  mutate(ds = as_date(ds)) %>%
  as_tsibble(key=id, index=ds)

daily_train_features <- daily_train %>% 
  features(y, list(
    feat_acf,
    feat_pacf,
    unitroot_ndiffs,
    unitroot_nsdiffs,
    var_tiled_mean,
    var_tiled_var,
    shift_level_max,
    feat_stl,
    feat_spectral,
    n_crossing_points,
    longest_flat_spot,
    coef_hurst,
    guerrero
  ))

write_csv(daily_train_features, "./data/processed/daily-train-features-r.csv")
  
ts <- daily_train %>%
  select(y) %>% 
  filter(id == 51)

ts %>% 
  autoplot(y)

ts_level_shift_info <- shift_level_max(ts$y)
level_shift_index = ts_level_shift_info[2]
level_shift_date = ts[[level_shift_index, 2]]

ts_kl_shift_info <- shift_kl_max(ts$y)
kl_shift_index = ts_kl_shift_info[2]
kl_shift_date = ts[[kl_shift_index, 2]]

ggplot(ts, mapping=aes(x=ds, y=y)) + 
  geom_line() + 
  geom_vline(
    xintercept = level_shift_date, 
    colour = "red",
    linetype = 4
  ) +
  geom_vline(
    xintercept = kl_shift_date, 
    colour = "blue",
    linetype = 4
  )

print(ts_level_shift_info)
print(ts_kl_shift_info)
