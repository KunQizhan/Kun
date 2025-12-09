library(tidyverse)     # for data manipulation and visualization
library(lubridate)     # for working with dates
# Read data set
bats_raw <- read_csv("dataset_Mata.et.al.2016.csv", na = "na")

## Question 1:
# A. Plot distribution of number of reads
q1_plot <- ggplot(bats_clean, aes(x = No_Reads)) + geom_histogram(binwidth = 5000)
print(q1_plot)
# D. Calculate mean and median
mean_reads <- mean(bats_clean$No_Reads, na.rm = TRUE)
median_reads <- median(bats_clean$No_Reads, na.rm = TRUE)
# E. Add vertical lines for mean and median
q1_plot_vlines <- q1_plot +
  geom_vline(aes(xintercept = mean_reads)) + geom_vline(aes(xintercept = median_reads))
print(q1_plot_vlines)

## Question 2:
# Count total reads per species
species_reads <- bats_clean %>% group_by(Species) %>% summarise(total_reads = sum(No_Reads, na.rm = TRUE))
# Calculate probability
species_reads <- species_reads %>% mutate(probability = total_reads / sum(total_reads))
# Step 3: Plot histogram
q2_plot <- ggplot(species_reads, aes(x = probability)) + geom_histogram(bins = 30)
print(q2_plot)
