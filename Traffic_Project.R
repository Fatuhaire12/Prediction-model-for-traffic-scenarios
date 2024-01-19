###
# identify patterns and trends over time in historical data 
# Load necessary libraries
library(dplyr)
library(tidyverse)
library(ggplot2)
library(lubridate)
#Change path here.
setwd("/home/fatumah/Dropbox/R_codes")#create a path
rm(list=ls())
#Load datasets.
#traffic <- read.csv(file = 'link road from A339 to M3 J6 roundabout 200053634.csv',header= TRUE)
traffic <- read.csv(file ='M3 westbound within J4A mainCarriageway 103050402.csv',header= TRUE)
head(traffic,1)

#Change Local.Time to DateTime
traffic$DateTime <- paste(traffic$Local.Date,traffic$Local.Time)
#PLot
ggplot(traffic, aes(x = DateTime, y = Fused.Average.Speed)) +
  geom_point() +
  labs(title = "Fused.Average.Speed Over Time",
       x = "Local.Time",
       y = "Fused.Average.Speed")

## Decompose the time series using seasonal decomposition of time series (STL)
decomposed_ts <-stl(ts(traffic$Fused.Average.Speed,freq=80), t.window=15, s.window="per", robust=TRUE)
# Plot the seasonal component
plot(decomposed_ts)
#Look at the trend of the data.
trend <- decomposed_ts$time.series[, "trend"]
plot(trend)
trend <- (decomposed_ts$seasonal)
seasonal <- decomposed_ts$time.series[, "seasonal"]
plot(seasonal)
##

# Assuming you want to create scenarios for different hours of the day
hourly_scenarios <- traffic %>%
  mutate(hour = hour(DateTime)) %>%
  group_by(hour) %>%   sample_n(size = 100, replace = FALSE)  # Adjust sample size as needed
#####
##Calculate the Average mean Fused.Average.Speed; in terms of hours
average_by_group <- hourly_scenarios %>% group_by(hour) %>% summarize(Average = mean( Fused.Average.Speed))
####

#Plot the average fused time versus hour
ggplot(average_by_group, aes(x = hour, y = Average)) +
  geom_line() +   labs(title = "Time-dependent traffic scenarios for junction j4",
                       x = "Hour",
                       y = "Time dependant average Fused.Average.Speed")

#Fit a generalized additive model (gam) on the fuse average speed and plot it.
ggplot(hourly_scenarios, aes(x = hour, y = Fused.Average.Speed)) +  geom_smooth(method = "gam")
#########

#Regression model. Relationship between speed and time.
modelT <- lm(traffic$Fused.Average.Speed ~ traffic$Fused.Travel.Time + 
               traffic$Profile.Travel.Time, data = traffic)#+ traffic$Link.Length 
summary(modelT)#summary of results

##### Scatter plot with regression lines
ggplot(traffic, aes(x = Fused.Travel.Time, y = Fused.Average.Speed)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "blue") +
  labs(x = "Fused.Travel.Time", y = "Fused.Average.Speed") +
  theme_minimal()

##### Scatter plot matrix
ggplot(traffic, aes(Fused.Average.Speed, Fused.Travel.Time, Profile.Travel.Time)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Fused.Average.Speed", y = "") +
  theme_minimal()
##### Residual plot
lm_fit <- lm(Fused.Average.Speed ~ Fused.Travel.Time + Profile.Travel.Time, data = traffic)
ggplot(traffic, aes(x = predict(lm_fit), y = residuals(lm_fit))) +
  geom_point() +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  labs(x = "Fitted values", y = "Residuals") +
  theme_minimal()
##############






