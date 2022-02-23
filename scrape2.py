import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import time

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

url = "https://www.imdb.com/search/title/?title_type=tv_episode&num_votes=600,&sort=user_rating,desc"

series_name = []
episode_name = []
genre = []
year = []
times = []
rating = []
votes = []
page = 1
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    episode_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
    for store in episode_data:
        h3=store.find('h3', attrs={'class': 'lister-item-header'})
        sName =h3.findAll('a')[0].text
        series_name.append(sName)
        eName = h3.findAll('a')[1].text
        episode_name.append(eName)

        year_of_release = h3.find('span', class_= 'lister-item-year text-muted unbold').find_next('span').text.replace('(', '').replace(')', '')
        year.append(year_of_release)

        runtime = store.p.find('span', class_ = "runtime").text.replace(' min', '') if store.find('span', class_ = "runtime") else 'N/A'
        times.append(runtime)

        showGenre = store.p.find('span', class_ = "genre").text.replace('\n', '').replace('            ', '') if store.find('span', class_ = "genre") else 'N/A'
        genre.append(showGenre)

        rate = store.find('div', class_ ='inline-block ratings-imdb-rating').text.replace('\n', '')
        rating.append(rate)

        value = store.find('span', attrs = {'name': 'nv'}).text
        votes.append(value)
    time.sleep(2)
    print(url)
    print(page)
    if (a := soup.select_one('a[href].next-page')):
        url = 'https://www.imdb.com'+a['href']
    else:
        break
    page += 50

episodes_DF = pd.DataFrame({'Show Name': series_name, 'Episode Name': episode_name, "Genre(s)": genre, "Watchtime (Min)": times, 'Year of Release': year, 
'Episode Rating': rating, 'Votes': votes})


episodes_DF.to_csv('episodes.csv', index=False)

df = pd.read_csv('episodes.csv')

data = df.to_dict(orient = "records")

db = client["TopEpisodes"]

db.episodes.insert_many(data)