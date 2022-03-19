library(dplyr)
library(rvest)
library(tidyverse)

getReviewLink = function(episodeLink) {
  Sys.sleep(1)
  tryCatch({
  episodePage = read_html(episodeLink)
  container = episodePage %>%
    html_nodes(".sc-1cdfe45a-9.cvYnNZ")
  
  reviewLinks = episodePage %>%
    html_nodes(".sc-1cdfe45a-9.cvYnNZ > ul > li:nth-child(1) > a") %>%
    html_attr("href") %>%
    paste("https://www.imdb.com", ., sep="")
  print(reviewLinks)
  
  cleanedReviewLink = ifelse(reviewLinks == "https://www.imdb.com", NA, reviewLinks)
  
  print(cleanedReviewLink)
  
  get_reviews = ifelse(is.na(cleanedReviewLink), NA, read_html(cleanedReviewLink) %>% html_nodes(".show-more__control") %>%
                         html_text() %>% str_trim())
  print(get_reviews)

  
  
  return(get_reviews)
  }, error = function(e){
    NA
  })
}

getNextUrl <- function(url) {
  read_html(url) %>% 
    html_node(".next-page") %>%
    html_attr("href") %>% 
    paste("https://www.imdb.com", ., sep="")
}


episodes = data.frame()
link = paste0("https://www.imdb.com/search/title/?title_type=tv_episode&num_votes=600,&sort=user_rating,desc&after=WzguMSwidHQwOTg4MjM3IiwxNjE1MV0%3D&ref_=adv_nxt")
while(TRUE){

  page = read_html(link)
  
  show_name = page %>% html_nodes(".lister-item-index+ a") %>% html_text() %>% str_trim
  
  episode_name = page %>% html_nodes("small+ a") %>% html_text()
  
  episode_links = page %>% html_nodes("small+ a") %>% html_attr("href") %>%
    paste("https://www.imdb.com", ., sep="")
  
  episodeReview = sapply(episode_links, FUN = getReviewLink, USE.NAMES = FALSE)
  
  print(episodeReview)
  
  episodes = rbind(episodes, data.frame(show_name, episode_name, episodeReview, stringsAsFactors = FALSE))
  
  link = getNextUrl(link)
  
  print(link)

  Sys.sleep(2)
  
  if (link == "https://www.imdb.comNA")
    break
  
}

#write.csv(episodes, "episodesReview.csv", sep = ",", row.names = FALSE)
write.table(episodes, file = "episodesReview.csv ", sep = ",", append = TRUE, row.names = FALSE)
