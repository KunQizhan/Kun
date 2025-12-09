# Exercises_Week-11.R
# Author: Kun
# Description: Answers to Week 11 exercises using the cleaned bats dataset

# Load necessary libraries / 载入必要的R包
library(tidyverse)     # for data manipulation and visualization / 用于数据处理和可视化
library(lubridate)     # for working with dates / 处理日期和时间

# ---------------------------
# Part 1: Data Cleaning / 第一部分：数据清洗
# ---------------------------

# Read original dataset / 读取原始数据集
bats_raw <- read_csv("dataset_Mata.et.al.2016.csv", na = "na")

# Clean column names and convert types / 清理列名，转换类型
bats_clean <- bats_raw %>%
  rename(
    Bat_ID = Sample,
    Wingspan = `Wingspan (mm)`,
    No_Reads = `No. Reads`,
    Date_proper = Date
  ) %>%
  mutate(
    Wingspan = as.numeric(Wingspan),               # Convert wingspan to numeric / 转换翼带长度
    Date_proper = ymd(Date_proper)                 # Format date / 时间格式化
  )

