import datetime
import re
import tweepy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#newspaper3k
from newspaper import Article
import nltk
nltk.download('punkt')

# Twitter Access Tokens

from config import *

# Connecting to twitter service

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class NewsArticle:
    text = ""
    keywords = []
    summary = ""
    title = ""

#using newpaper3k module to get text,title,summary and keywords
#from the article/url link
def news3k(url):
    newsarticle = NewsArticle()
    article = Article(url)
    article.download()
    article.parse()
    newsarticle.title = article.title
    newsarticle.text = article.text
    article.nlp()
    newsarticle.keywords = article.keywords
    newsarticle.summary = article.summary
    return newsarticle

#get colorcode for polarity and subjectivity
# <0 red, >0 green
def getColor(val):
    if val>0: 
        return 'g'
    else: 
        return 'r'

# Getting tredning News
def update():
    url = 'https://in.reuters.com/news/top-news'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all(href=re.compile('/article/'))

    base_url = "https://in.reuters.com/"
    article_links = []

    links.pop()
    links.pop()

    for i in links:
        if 'Continue Reading' in i.text:
            pass
        else:
            article_links.append(base_url + i['href'])

    for i in article_links:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        temp = soup.findAll('p')
        print(i)
        articleNews = news3k(i)
        blob = TextBlob(articleNews.text).sentiment
        polarity = blob[0]
        subjectivity = blob[1]
        bar = plt.bar(['Polarity', 'Subjectivity'], [polarity, subjectivity])
        bar[0].set_color(getColor(polarity))
        bar[1].set_color(getColor(subjectivity))
        plt.title(articleNews.title)
        plt.savefig('Dude.png')
        plt.clf()
        api.update_with_media('Dude.png', "This is the polarity and subjectivity on the topic " + links[
            article_links.index(i)].text +
                              " by reuters #Reuters #Analysis")
update()

def updateHindustanTimes():
    url = 'https://www.hindustantimes.com/rss/topnews/rssfeed.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')
    items=soup.find_all('item')

    article_links = []
    headings=[]


    for i in items:
        headings.append(i.find('title').text)
        link=(i.find('link')).text
        print(i.find('title').text)
        article_links.append(link)
        
    for i in article_links:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        #temp = soup.findAll('p')
        print(i)
        articleNews = news3k(i)
        blob = TextBlob(articleNews.text).sentiment
        polarity = blob[0]
        subjectivity = blob[1]
        bar = plt.bar(['Polarity', 'Subjectivity'], [polarity, subjectivity])
        bar[0].set_color(getColor(polarity))
        bar[1].set_color(getColor(subjectivity))
        plt.title(articleNews.title)
        plt.show()
        plt.savefig('htnews.png')
        plt.clf()

#     api.update_with_media('Dude.png', "This is the polarity and subjectivity on the topic " + links[
#         article_links.index(i)].text +
#                           " by reuters #Reuters #Analysis")
        
# while True:
#     currentDT = str(datetime.datetime.now())
#     hours = currentDT.split(" ")[1].split(':')[0]
#     minutes = currentDT.split(" ")[1].split(':')[1]
#     seconds = int(float(currentDT.split(" ")[1].split(':')[-1]))
#     if hours == '20' and minutes == '00' and seconds == 0:
#         update()


# newsarticle = news3k('https://in.reuters.com/article/soccer-worldcup-bra-bel/soccer-belgium-hold-off-brazil-in-thriller-to-reach-semis-idINKBN1JW2UO')
# print(newsarticle.keywords)
# print("\n"+newsarticle.text)
# print("\n"+newsarticle.title)
