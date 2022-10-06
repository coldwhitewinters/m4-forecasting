library("tidyverse")
library("tsibble")
library("fable")
library("feasts")
library("lubridate")
library("optparse")

option_list = list(
    make_option(
        c("-f", "--file"),
        type="character",
        default=NULL,
        help="input file name",
        metavar="character"
    )
)

opt_parser = OptionParser(option_list = option_list)
opt = parse_args(opt_parser)

if (is.null(opt$file)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input file).n", call. = FALSE)
}

input_filename <- opt$file
base_dir <- "./data/processed/base"
features_dir <- "./data/processed/features"
dir.create(features_dir, showWarnings = FALSE)

tbl <- read_csv(file.path(base_dir, input_filename))

if (grepl("Hourly", input_filename)) {
    parse_date_f <- as_datetime
} else if (grepl("Daily", input_filename)) {
    parse_date_f <- as_date
} else if(grepl("Weekly", input_filename)) {
    parse_date_f <- yearweek
} else if(grepl("Monthly", input_filename)) {
    parse_date_f <- yearmonth
} else if(grepl("Quarterly", input_filename)) {
    parse_date_f <- yearquarter
} else if(grepl("Yearly", input_filename)) {
    parse_date_f <- as_date
}

index <- "date"
if (any(map_lgl(tbl$date, is.na))) {
    warning("Date fields have NA. Time step will be used as index.")
    index <- "t"
}

tsbl <- tbl %>%
    select(-category) %>%
    mutate(date = parse_date_f(date)) %>%
    as_tsibble(
        key = name,
        index = index
    )

print("Glance at the input data:")
print(tsbl)

# tsbl <- tsbl %>% filter(name %in% unique(tsbl$name)[1:3])

print("Generating features...")

tbl_features <- tsbl %>%
    features(
        y,
        features = feature_set(pkgs = "feasts")
    )

len_name <- nchar(input_filename)
name <- substr(input_filename, 1, len_name-4)
ext <- substr(input_filename, len_name-3, len_name)
output_filename <- paste0(name, "-features", ext)

write_csv(tbl_features, file.path(features_dir, output_filename))
