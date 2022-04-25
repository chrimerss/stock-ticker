# Import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd
import matplotlib.pyplot as plt
# NLTK VADER for sentiment analysis
import nltk
# nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

finwiz_url = 'https://finviz.com/quote.ashx?t='
vader= SentimentIntensityAnalyzer()

def get_sentiment(ticker):
    url = finwiz_url + ticker
    req= Request(url=url, headers={'User-Agent': 'Chrome/100.0.4896.127'})
    response= urlopen(req)
    html= BeautifulSoup(response)
    # loop through and find useful news item
    news_table= html.find(id='news-table')
    parsed_news= pd.DataFrame( columns=['ticker', 'date', 'time', 'headline'])
    for i, x in enumerate(news_table.findAll('tr')):
        parsed_news.loc[i,'headline']= x.a.get_text()
        date_scrape= x.td.text.split()
        if len(date_scrape) == 1:
            parsed_news.loc[i, 'time']= date_scrape[0]
            parsed_news.loc[i, 'date']= date
        else:
            date = date_scrape[0]
            parsed_news.loc[i, 'date']= date_scrape[0]
            parsed_news.loc[i, 'time']= date_scrape[1]
        score= vader.polarity_scores(x.a.get_text())
        # print(score)
        parsed_news.loc[i,'ticker']= ticker
        parsed_news.loc[i,'pos']= score['pos']
        parsed_news.loc[i,'neg']= score['neg']
        parsed_news.loc[i,'neu']= score['neu']
        parsed_news.loc[i,'compound']= score['compound']
        # parsed_news.loc[i, 'score']= vader.polarity_scores(x.a.get_text())
    
    return parsed_news


if __name__=='__main__':
    df= get_sentiment('AAPL')
    print(df)
        

    

