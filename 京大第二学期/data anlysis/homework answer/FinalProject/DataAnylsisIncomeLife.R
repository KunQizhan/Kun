# Load required libraries
library(tidyverse)
library(dplyr)
library(ggplot2)

# Read datasets
life <- read_csv("life-expectancy.csv")
income <- read_csv("world-bank-income-groups.csv")
happy <- read_csv("happiness-cantril-ladder.csv")

# Data cleaning and renaming columns
life <- life %>% rename(Country = Entity, LifeExpectancy = `Period life expectancy at birth - Sex: total - Age: 0`)
income <- income %>% rename(Country = Entity, IncomeGroup = `World Bank's income classification`)
happy <- happy %>% rename(Country = Entity, LifeSatisfaction = `Cantril ladder score`)

# Merge data and handle missing values
merged_data <- life %>%
  inner_join(income, by = c("Country", "Code", "Year")) %>%
  inner_join(happy, by = c("Country", "Code", "Year")) %>%
  mutate(
    LifeExpectancy = as.numeric(LifeExpectancy),
    LifeSatisfaction = as.numeric(LifeSatisfaction)
  ) %>%
  drop_na(LifeExpectancy, IncomeGroup, LifeSatisfaction)

# Q1
trend <- merged_data %>%
  group_by(IncomeGroup, Year) %>%
  summarise(
    AverageLife = mean(LifeExpectancy, na.rm = TRUE),
    AvgSatisfaction = mean(LifeSatisfaction, na.rm = TRUE),
    .groups = "drop"
  )

# Plot: Life Expectancy Trend
ggplot(trend, aes(x = Year, y = AverageLife, color = IncomeGroup)) +
  geom_line(size = 1.2) +
  geom_point(size = 1.8) +
  labs(
    title = "Life Expectancy Trends by World Bank Income Groups",
    x = "Year",
    y = "Average Life Expectancy (Years)",
    color = "Income Group"
  ) +
  theme_minimal()

# Plot: Life Satisfaction Trend
ggplot(trend, aes(x = Year, y = AvgSatisfaction, color = IncomeGroup)) +
  geom_line(size = 1.2) +
  geom_point(size = 1.8) +
  labs(
    title = "Life Satisfaction Trend by Income Group",
    x = "Year",
    y = "Average Life Satisfaction"
  ) +
  theme_minimal()

# Q2
ggplot(merged_data, aes(x = LifeExpectancy, y = LifeSatisfaction, color = IncomeGroup)) +
  geom_point(alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Correlation between Life Expectancy and Life Satisfaction",
    x = "Life Expectancy (Years)",
    y = "Life Satisfaction Score"
  ) +
  theme_minimal()

# Q3.
variability <- merged_data %>%
  group_by(IncomeGroup, Year) %>%
  summarise(SatSD = sd(LifeSatisfaction, na.rm = TRUE), .groups = "drop")

ggplot(variability, aes(x = Year, y = SatSD, color = IncomeGroup)) +
  geom_line(size = 1.2) +
  geom_point(size = 1.8) +
  labs(
    title = "Within-group Life Satisfaction Variability over Time",
    x = "Year",
    y = "Standard Deviation of Satisfaction"
  ) +
  theme_minimal()

# Q4
gap_data <- merged_data %>%
  filter(IncomeGroup %in% c("High-income countries", "Low-income countries")) %>%
  group_by(IncomeGroup, Year) %>%
  summarise(AverageLife = mean(LifeExpectancy, na.rm = TRUE), .groups = "drop") %>%
  tidyr::pivot_wider(names_from = IncomeGroup, values_from = AverageLife) %>%
  mutate(LifeGap = `High-income countries` - `Low-income countries`)

ggplot(gap_data, aes(x = Year, y = LifeGap)) +
  geom_line(color = "red", size = 1) +
  geom_point(color = "darkred") +
  labs(
    title = "Life Expectancy Gap (High vs Low Income) Over Time",
    x = "Year",
    y = "Life Expectancy Gap (Years)"
  ) +
  theme_minimal()

# Q5
ggplot(merged_data, aes(x = LifeSatisfaction, fill = IncomeGroup)) +
  geom_density(alpha = 0.5) +
  labs(
    title = "Distribution of Life Satisfaction by Income Group",
    x = "Life Satisfaction Score",
    y = "Density"
  ) +
  theme_minimal()

# Q6
ggplot(merged_data, aes(x = LifeExpectancy, y = LifeSatisfaction, color = IncomeGroup)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "loess", se = FALSE, size = 1) +
  labs(
    title = "Non-linear Relationship Between Life Expectancy and Satisfaction",
    x = "Life Expectancy (Years)",
    y = "Life Satisfaction Score"
  ) +
  theme_minimal()

# Q7
life_sd <- merged_data %>%
  group_by(IncomeGroup, Year) %>%
  summarise(SD_Life = sd(LifeExpectancy, na.rm = TRUE), .groups = "drop")

ggplot(life_sd, aes(x = Year, y = SD_Life, color = IncomeGroup)) +
  geom_line(size = 1) +
  geom_point() +
  labs(
    title = "Within-group Life Expectancy Variability Over Time",
    x = "Year",
    y = "Standard Deviation of Life Expectancy"
  ) +
  theme_minimal()

# Q8
life_gain <- merged_data %>%
  filter(IncomeGroup == "Low-income countries") %>%
  group_by(Country) %>%
  summarise(
    Gain = max(LifeExpectancy, na.rm = TRUE) - min(LifeExpectancy, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(Gain)) %>%
  slice(1:10)

ggplot(life_gain, aes(x = reorder(Country, Gain), y = Gain)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(
    title = "Top 10 Low-income Countries by Life Expectancy Improvement",
    x = "Country",
    y = "Life Expectancy Gain (Years)"
  ) +
  theme_minimal()
