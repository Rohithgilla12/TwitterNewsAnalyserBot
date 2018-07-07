import datetime
import re
import tweepy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib
from fuzzywuzzy import fuzz
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

# Getting tredning News from reuters

article_links=[]
list_of_titles=[]
def updateReuters():
    url = 'https://in.reuters.com/news/sports'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all(href=re.compile('/article/'))
    base_url = "https://in.reuters.com/"
    global article_links
    global list_of_titles

    links.pop()
    links.pop()

    for i in links:
        if 'Continue Reading' in i.text:
            pass
        else:
            news_url=base_url + i['href']
            title_text=i.text
            # print("url is ",news_url)
            # print("title is ",title_text)
            if title_text:
                article_links.append(news_url)
                list_of_titles.append(title_text)
#                 print(title_text,":",news_url)




'''
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
'''



ht_headings=[]
ht_article_links=[]

def updateHindustanTimes():
    url = 'https://www.hindustantimes.com/rss/sports/rssfeed.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')
    items=soup.find_all('item')




    global ht_article_links
    global ht_headings


    for i in items:
        ht_headings.append(i.find('title').text)
        link=(i.find('link')).text
#         print(i.find('title').text)
        ht_article_links.append(link)
    
'''
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
'''
        
def compare(title1_list,link1_list,title2_list,link2_list):
    compare_dict=[]
    for title1 in title1_list:
        maxVal=10
        t1=title1
        l1=link1_list[title1_list.index(title1)]
        t2=""
        l2=""
        for title2 in title2_list:
            val=fuzz.ratio(title1, title2)                
            if maxVal<val:
                t2=title2
                l2=link2_list[title2_list.index(title2)]
                maxVal=val
        temp_dict={}
        temp_dict["title1"]=t1
        temp_dict["link1"]=l1
        temp_dict["title2"]=t2
        temp_dict["link2"]=l2
        temp_dict["score"]=maxVal
        compare_dict.append(temp_dict)
#     print(compare_dict)
    
#     for i in compare_dict:
#         print(i)
#         print()
    return compare_dict        
        
def plot_similar_news(compared_dict):
    for news_item in compared_dict:
        ht_title1=news_item["title1"]
        ht_link1=news_item["link1"]
        rt_title2=news_item["title2"]
        rt_link2=news_item["link2"]
        
        
        #for ht
        articleNews = news3k(ht_link1)
        blob = TextBlob(articleNews.text).sentiment
        ht_polarity = blob[0]
        ht_subjectivity = blob[1]

        #for reu
        articleNews = news3k(rt_link2)
        blob = TextBlob(articleNews.text).sentiment
        rt_polarity = blob[0]
        rt_subjectivity = blob[1]
        
        plt.bar(['Polarity_ht', 'Subjectivity_ht','Polarity_reu', 'Subjectivity_reu'], [ht_polarity, ht_subjectivity,rt_polarity,rt_subjectivity])
        title=ht_title1+" VS "+rt_title2
        plt.title(title)
        #plt.show()
        plt.savefig('htnews.png')
        plt.clf()
        api.update_with_media('htnews.png', "This is the polarity and subjectivity on the topic " + title +
                           " by reuters #Reuters #Analysis")


        





        
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

updateReuters()
updateHindustanTimes()
compared_dict=compare(ht_headings,ht_article_links, list_of_titles,article_links)
plot_similar_news(compared_dict)   

