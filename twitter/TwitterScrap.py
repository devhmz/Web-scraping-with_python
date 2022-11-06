import snscrape.modules.twitter as twitterScraper
import snscrape.modules.instagram as instagramScraper
import snscrape.modules.facebook as facebookScraper 
import json 
import pandas as pd 
from time import time
import csv as csv
import re
# Twitter 

# Initialisation d'un tableau de données 
tweet_data = []

# Demande d'information au utilisateur 
hashtag = input('Entrez votre hashtag: ')
data_size = int(input('Entrez le nombre de tweets: '))

# Extraction de données (limité à data_size )
for i, tweets in enumerate(twitterScraper.TwitterSearchScraper('{}'.format(hashtag)).get_items()):
    if i > data_size:
        break
    # tweet_data.append([tweets.date, tweets.content, tweets.user.username, tweets.url]) 
    tweet_data.append([tweets.content]) 

#https = 'https'
# Enregistrement des données dans un fichier CSV
# df = pd.DataFrame(tweet_data, columns=['Date', 'Tweets', 'Username', 'Url'])
df = pd.DataFrame(tweet_data, columns=['Tweets'])
df.to_csv("avis.csv", index=False, encoding='utf-8')

regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

tab = []

fp = open("avis.csv", "r", encoding="utf-8")
for ligne in csv.reader(fp, delimiter=";"):
    for i in ligne : 
         text =  re.sub(r'@[A-Za-z0-9]+',' ',i) #removes the @mentions
         text =  re.sub(r'#',' ',text) #removes the hashtags
         text =  re.sub(r'RT[\s]+',' ',text) #removes the retweets
         text =  re.sub(r'https?://\S+',' ',text) #removes the hyper links
         text = text.lower()
         text = text.replace('\n', ' ').replace('\r', '')
         text = ' '.join(text.split())
         text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text)
         text = re.sub(r"(\s\-\s|-$)", "", text)
         text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)
         text = re.sub(r"\&\S*\s", "", text)
         text = re.sub(r"\&", "", text)
         text = re.sub(r"\+", "", text)
         text = re.sub(r"\#", "", text)
         text = re.sub(r"\$", "", text)
         text = re.sub(r"\£", "", text)
         text = re.sub(r"\%", "", text)
         text = re.sub(r"\:", "", text)
         text = re.sub(r"\@", "", text)
         text = re.sub(r"\-", "", text)
         tab.append([text])
        
df = pd.DataFrame(tab, columns=['Tweets'])
df.to_csv("avis_nettoyes1.csv", index=False, encoding='utf-8')
      
        


    
    # for cellule in ligne:
    #url = re.search("https", ligne)
    # url = re.findall(regex, ligne)
    # print(url) 
    # if  re.sub(r'https?://\S+',' ',ligne) : 
    #     print("ok")
    # else :
    #     print("error")  
        
