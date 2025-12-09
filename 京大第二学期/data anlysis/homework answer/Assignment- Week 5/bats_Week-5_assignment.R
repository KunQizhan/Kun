library(dplyr)
library(ggplot2)
library(readr)
library(stringr)
library(lubridate)
library(tidyr)
library(ggbeeswarm)

bats <- read_csv("dataset_Mata.et.al.2016.csv", na = "na")

glimpse(bats)

bats %>% 
  select(`Wingspan (mm)`) %>% 
  head(10)

bats <- bats %>%
  rename(Bat_ID = Sample)

bats <- bats %>%
  rename(Row_order = `Order`,
         Order = `Order_1`)

names(bats) <- str_replace_all(names(bats), c(" " = "_"))

names(bats) <- str_replace_all(names(bats), c("\\(" = "", "\\)" = ""))

bats <- bats %>%
  mutate(Date_proper = ymd(Date))

bats <- bats %>%
  select(-Date)

bats <- bats %>%
  mutate(Sex = case_when(Sex == "M" ~ "Male",
                         Sex == "F" ~ "Female"))

bats <- bats %>%
  mutate(Age = case_when(Age == "Ad" ~ "Adult",
                         Age == "Juv" ~ "Juvenile"))

bats %>%
  duplicated() %>%
  sum()

bats %>%
  select(Bat_ID, Sp._Nr., Date_proper) %>%
  duplicated() %>%
  sum()

bats %>%
  summarise(var_min = min(Wingspan_mm, na.rm = TRUE),
            var_max = max(Wingspan_mm, na.rm = TRUE))


bats %>%
  distinct(Sex)

bats %>%
  summarise(num_nas = sum(is.na(Wingspan_mm)))

(bats %>%
    summarise(across(everything(), ~sum(is.na(.))))) %>%
  write_csv("my_clean_bats.csv")

