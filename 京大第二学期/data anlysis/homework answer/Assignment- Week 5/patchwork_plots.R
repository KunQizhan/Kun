##Question 1
library(ggplot2)
library(patchwork)
library(readr)

bats <- read_csv("dataset_Mata.et.al.2016.csv", na = "na")

p1 <- ggplot(bats, aes(x = `Wingspan (mm)`)) + geom_histogram(binwidth = 5) + ggtitle("Histogram")
p2 <- ggplot(bats, aes(x = Sex, y = `Wingspan (mm)`)) + geom_boxplot() + ggtitle("Boxplot")
p3 <- ggplot(bats, aes(x = `Wingspan (mm)`, fill = Sex)) + geom_density(alpha = 0.4) + ggtitle("Density")
p4 <- ggplot(bats, aes(x = Sex, y = `Wingspan (mm)`)) + geom_violin() + ggtitle("Violin Plot")

combined_plot <- (p1 | p2) / (p3 | p4)

ggsave("week5_patchwork.pdf", combined_plot, width = 10, height = 8)