import re
import tweepy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import datetime

# Twitter Access Tokens

consumer_key = "Key"
consumer_secret = "Key"
access_token = "Key"
access_token_secret = "Key"

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

while True:
    currentDT = str(datetime.datetime.now())
    hours = currentDT.split(" ")[1].split(':')[0]
    minutes = currentDT.split(" ")[1].split(':')[1]
    seconds = int(float(currentDT.split(" ")[1].split(':')[-1]))
    if(hours=='20' and minutes=='00' and seconds==0):
        update()
