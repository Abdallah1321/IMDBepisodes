import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import time

import pymongo

# initizialise mongo connection

client = pymongo.MongoClient("mongodb://localhost:27017")

# url which is used to get data from 

url = "https://www.imdb.com/search/title/?title_type=tv_episode&num_votes=600,&sort=user_rating,desc"

# declare the features which will be extracted from IMDB
rank = []
series_name = []
episode_name = []
genre = []
year = []
times = []
rating = []
votes = []
page = 1

# loop to get through all the pages

while True:

    # sends request to access the IMDB page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # stores the data in a variable to extract the seperate features

    episode_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

    # for loop to loop through each item from all the data on the page

    for store in episode_data:
        # define h3 as the h3 element to avoid redundancy

        h3=store.find('h3', attrs={'class': 'lister-item-header'})
        
        ranks = h3.find('span', class_ = 'lister-item-index unbold text-primary').text.replace('.', '')
        rank.append(ranks)

        sName =h3.findAll('a')[0].text.strip()
        series_name.append(sName)
        eName = h3.findAll('a')[1].text
        episode_name.append(eName)

        year_of_release = h3.find('span', class_= 'lister-item-year text-muted unbold').find_next('span').text.replace('(', '').replace(')', '')
        year.append(year_of_release)

        # Some episodes do not have an age rating so if statement is added to write over all the empty variables with "N/A"
        
        # replace function is used to clean up the code and remove characters which are not needed

        runtime = store.p.find('span', class_ = "runtime").text.replace(' min', '') if store.find('span', class_ = "runtime") else 'N/A'
        times.append(runtime)

        showGenre = store.p.find('span', class_ = "genre").text.replace('\n', '').replace('            ', '') if store.find('span', class_ = "genre") else 'N/A'
        genre.append(showGenre)

        rate = store.find('div', class_ ='inline-block ratings-imdb-rating').text.replace('\n', '')
        rating.append(rate)

        value = store.find('span', attrs = {'name': 'nv'}).text
        votes.append(value)
    
    # time library is used to make the program wait before going to the next page, so the program is not seen as a bot and
    # connection time out is avoided

    time.sleep(2)
    print(url)
    print(page)

    # if statement is used to check if the href for the next page button, and if next page button is found, url is replaced
    # with the url to the next page and the loop continues, otherwise, break from the loop

    if (a := soup.select_one('a[href].next-page')):
        url = 'https://www.imdb.com'+a['href']
    else:
        break
    page += 50

# convert all the data gathered to a dataframe using the pandas library

episodes_DF = pd.DataFrame({'Rank': rank,'Show Name': series_name, 'Episode Name': episode_name, "Genre": genre, 
"Watchtime (Min)": times, 'Year of Release': year, 'Episode Rating': rating, 'Votes': votes})

# since genre column has multiple genre's, we split up each genre into seperate columns

episodes_DF[["Genre 1", "Genre 2", "Genre 3"]] = episodes_DF['Genre'].str.split(',', expand=True)

# we then delete the genre column as it becomes redundant with the multiple genre columns

episodes_DF.drop('Genre', inplace = True, axis = 1)

# convert dataframe to csv file

episodes_DF.to_csv('NewEpisodes.csv', index=False)

df = pd.read_csv('NewEpisodes.csv')

# convert the data frame to a dictionary to allow it to be inserted into database

data = df.to_dict(orient = "records")

# Create a database in Mongo called TopEpisodes to store the dataframe

db = client["NewTopEpisodes"]

# create a collection called episodes and insert all the data into the database

db.episodes.insert_many(data)