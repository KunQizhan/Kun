library(readr)
library(tidyverse)
df <- read_csv("data/pisa-test-score-mean-performance-on-the-science-scale (1).csv")

##Question 1
df <- df %>% rename(Country = 1, Score = 4)


##Question 2
### The total number of distinct countries and years of data in the dataset
summary_overall <- df %>% summarise(n_countries = n_distinct(Country), n_years = n_distinct(Year))
print(summary_overall)

### The mean, min, and max scores (overall, for all countries together)
overall_stats <- df %>% summarise(mean_score = mean(Score, na.rm = TRUE),min_score  = min(Score,  na.rm = TRUE),max_score  = max(Score,  na.rm = TRUE))
print(overall_stats)

### The mean and median score for each individual country
country_stats <- df %>% group_by(Country) %>% summarise(mean_score   = mean(Score,   na.rm = TRUE),median_score = median(Score, na.rm = TRUE)) %>% arrange(desc(mean_score))
print(country_stats)


## Question 3
### Select the data for Japan and Canada using filter(), putting the results in new object 
#(Hint: You may need to use | (as logical “or”) to select two countries)
df_jp_ca <- df %>% filter(Country == "Japan" | Country == "Canada")

### Summarize the mean score for the two countries
df_jp_ca %>% group_by(Country) %>% summarise(mean_score = mean(Score, na.rm = TRUE))
df_jp_ca %>% summarise(mean_score_all = mean(Score, na.rm = TRUE))


## Question 4
## Prepare three different plots to display the selected data using:
### geom_line() showing scores for Japan and Canada for all years in the dataset. Use color = Country as option.
p1 <- ggplot(df_jp_ca, aes(x = Year, y = Score, color = Country)) + geom_line(size = 1) + labs(title = "Japan vs Canada: Science Score Over Time", x = "Year", y = "Score")
ggsave("plot_line.png", p1, width = 6, height = 4, dpi = 300)

### geom_boxplot() to compare scores between Japan and Canada
p2 <- ggplot(df_jp_ca, aes(x = Country, y = Score, fill = Country)) + geom_boxplot() + labs(title = "Score Distribution: Japan vs Canada", x = NULL, y = "Score") + theme(legend.position = "none")
ggsave("plot_boxplot.png", p2, width = 4, height = 4, dpi = 300)

### geom_point() to compare scores between Japan and Canada
p3 <- ggplot(df_jp_ca, aes(x = Country, y = Score)) + geom_point(position = position_jitter(width = 0.1), alpha = 0.6) + labs(title = "Score Points: Japan vs Canada", x = NULL, y = "Score")
ggsave("plot_point.png", p3, width = 4, height = 4, dpi = 300)