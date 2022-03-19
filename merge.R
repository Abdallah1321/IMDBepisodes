library(tidyverse)
library(rvest)
library(dplyr)

df1 = read.csv('NewEpisodes.csv', head = T)
df2 = read.csv('episodesReview.csv', head = T, )
df2 = df2[, c("Episode.Name", "Show.Name", "Episode.Review")]

newDF = merge(df1, df2, by = c("Episode.Name", "Show.Name"), all.x = TRUE)

dfLeft = df1 %>% left_join(df2, by=c("Episode.Name", "Show.Name"))

write.csv(dfLeft, "EpisodesData.csv", sep = ",", row.names = FALSE)
