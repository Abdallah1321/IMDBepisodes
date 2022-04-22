# IMDBepisodes
This is my big data project, which started with me scraping 60,000 records. 30,000 of episode data, and another 30,000 containing the reviews of those episodes.

After scraping all this data, I merged the csv file to a file with around 32,000 records, containing all the episode data as well as the reviews.

View the dashboard for yourself!

**Dashboard link:** https://abdallahsepisodes.herokuapp.com/

### Hadoop folder
This folder contains the necessary files to create a docker image and put the data into a hive server.

### Assets folder
This folder contains the css for the dashboard app.

### All csv files
Contains the data for the episodes through all the stages of the project.

### SentimentAnalysis2.ipynb
This file is the jupyter notebook file where the sentiment analysis for the the episode reviews is done. Sentiment analysis is done using textblob.

### app.py
This file is where the dashboard is created and is created using dash: plotly.

### eda.ipynb
This file is where the exploratory data analysis for the data is done and visualises the data as well as cleans the data.

### merge.R
This file was used for merginf the csv files after the initial scraping.

### rscrape.R
This is the webscraper which gets the reviews of the episode.

### scrape2.py
This is the webscraper which scrapes all the episode data except for the episode review.
