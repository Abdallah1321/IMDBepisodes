library(rvest)
library(dplyr)

link = "https://www.imdb.com/search/title/?title_type=tv_episode&num_votes=1000,&sort=user_rating,desc&start=1&ref_=adv_nxt"
page = read_html(link)

show_name = page %>% html_nodes(".lister-item-header a"[1]) %>% html_text()