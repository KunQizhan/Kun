# First we load a required package (we need to install this if we haven't already)
library(readr)
# also we will use some other packages
library(dplyr)
library(ggplot2)

# Now read in the data, using the read_csv() function and store it in class_RTs.
class_RTs <- read_csv("data/RT_data_insights_2025.csv")

# Have a look at the data in R
#View(class_RTs)
# or just do
class_RTs
glimpse(class_RTs)
View(class_RTs)

# Must be very careful to get the next line right!!! Really important!!!
names(class_RTs) <- c("Timestamp", "ID", "Sex", "Age", "Handedness", "Pref_Reaction_time_1", "Pref_Reaction_time_2",
                      "Pref_Reaction_time_3",  "Pref_Reaction_time_4", "Pref_Reaction_time_5","Pref_Reaction_time_ave")
                      
class_RTs
glimpse(class_RTs)

# Have to do this live!!!
# e.g. to exclude observations with character entries in Reaction_time variable
class_RTs <- filter(class_RTs, !is.na(as.numeric(Pref_Reaction_time_ave)))

# try using type_convert() from readr package.
class_RTs <- type_convert(class_RTs)

# Check numbers of data points in each sex by extracting column for Sex using $
table(class_RTs$Sex) # this is base R to get the counts at each combination of factor level, here Sex.

#check number of observations
class_RTs

# Verify that user entered mean fits entered data points by calculating Mean in a new column
class_RTs <- mutate(class_RTs, Mean = rowMeans(class_RTs[,6:10 ]))

class_RTs <- filter(class_RTs, (Pref_Reaction_time_ave < 1000)) # remove unexpected values as needed

#plot histrogram of data
ggplot() +
  geom_histogram(data = class_RTs, aes(x=Pref_Reaction_time_ave))

# Separate the histograms for each sex:
ggplot() +
  geom_histogram(data = class_RTs, aes(x=Pref_Reaction_time_ave), binwidth = 10) + 
  facet_wrap(~ Sex) #, binwidth = 20

# box and whisker plot
ggplot() +
  geom_boxplot(data = class_RTs, aes(x=Sex, y=Pref_Reaction_time_ave)) 

# raw data points plot
ggplot() +
  geom_jitter(data = class_RTs,
              aes(x=Sex, y=Pref_Reaction_time_ave),
              width=0.05)

#Let's get some basic statistics to wrap it up
#getting the mean
class_RTs %>% group_by(Sex) %>%
  summarise(mean_RT=mean(Pref_Reaction_time_ave),
            sd_RT=sd(Pref_Reaction_time_ave))

# t-test
my_ttest <- t.test(Pref_Reaction_time_ave ~ Sex, data=class_RTs, var.equal=TRUE)
my_ttest

#Final graph (with proper y-axis label)
ggplot() +
  geom_boxplot(data = class_RTs,
               aes(x=Sex, y=Pref_Reaction_time_ave)) +
  ylab("Reaction time (milliseconds)")

