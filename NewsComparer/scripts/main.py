import datetime
import re
import tweepy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Twitter Access Tokens

from config import *

# Connecting to twitter service

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


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
        message = links[article_links.index(i)].text + "\n"
        for j in temp:
            message += j.text + '\n'
        blob = TextBlob(message).sentiment
        polarity = blob[0]
        subjectivity = blob[1]
        plt.bar(['Polarity', 'Subjectivity'], [polarity, subjectivity])
        plt.title(links[article_links.index(i)].text)
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
        temp = soup.findAll('p')

        
        indx=article_links.index(i)
        message = headings[indx]
        
        for j in temp:
            message += j.text + '\n'
        blob = TextBlob(message).sentiment
        polarity = blob[0]
        subjectivity = blob[1]
        plt.bar(['Polarity', 'Subjectivity'], [polarity, subjectivity])
        plt.title(headings[indx])
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

# newsarticle = news3k('https://in.reuters.com/article/soccer-worldcup-bra-bel/soccer-belgium-hold-off-brazil-in-thriller-to-reach-semis-idINKBN1JW2UO')
# print(newsarticle.keywords)
# print("\n"+newsarticle.text)
# print("\n"+newsarticle.title)
