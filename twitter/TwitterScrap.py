import snscrape.modules.twitter as twitterScraper
import snscrape.modules.instagram as instagramScraper
import snscrape.modules.facebook as facebookScraper 
import json 
import pandas as pd 
from time import time
import csv as csv
import re
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import matplotlib.pyplot as plt
import numpy as np
 
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




# Cleaning data 

tab = []
fp = open("avis.csv", "r", encoding="utf-8")
for ligne in csv.reader(fp, delimiter=";"):
    for i in ligne : 
         text =  re.sub(r'@[A-Za-z0-9]+',' ',i) #removes the @mentions
         text =  re.sub(r'#',' ',text) #removes the hashtags
         text =  re.sub(r'RT[\s]+',' ',text) #removes the retweets
         text =  re.sub(r'https?://\S+',' ',text) #removes the hyper links
         text = text.lower() # removes lower case
         text = text.replace('\n', ' ').replace('\r', '') #removes sapces
         text = ' '.join(text.split()) #split string
         text = re.sub(r"[A-Za-z\.]*[0-9]+[A-Za-z%°\.]*", "", text) #removes the @mentions
         text = re.sub(r"(\s\-\s|-$)", "", text) #removes the $mentions
         text = re.sub(r"[,\!\?\%\(\)\/\"]", "", text)  #removes the \\\\mentions
         text = re.sub(r"\&\S*\s", "", text) #removes the &*mentions
         text = re.sub(r"\&", "", text)#removes the &mentions
         text = re.sub(r"\+", "", text)#removes the +mentions
         text = re.sub(r"\#", "", text)#removes the #mentions
         text = re.sub(r"\$", "", text)#removes the $mentions
         text = re.sub(r"\£", "", text)#removes the £mentions
         text = re.sub(r"\%", "", text)#removes the %mentions
         text = re.sub(r"\:", "", text)#removes the :mentions
         text = re.sub(r"\@", "", text)#removes the @mentions
         text = re.sub(r"\-", "", text)#removes the -mentions
         tab.append([text])
        
df = pd.DataFrame(tab, columns=['Tweets'])
df.to_csv("avis_nettoyes1.csv", index=False, encoding='utf-8')

#Sentiment analysis
tweets = pd.read_csv("avis_nettoyes1.csv")
corpus = df['Tweets']

polarity = []

for tweet in corpus:
  polarity.append(TextBlob(tweet,pos_tagger=PatternTagger(),analyzer=PatternAnalyzer()).sentiment[0])      

print(polarity)

# Visualisation of result

plt.plot(polarity)


# If you want to use regex , here is an exepmle 
#regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"


    # rechercher les liens dans les commanatiares 
    # for cellule in ligne:
    #url = re.search("https", ligne)
    # url = re.findall(regex, ligne)
    # print(url) 
    # if  re.sub(r'https?://\S+',' ',ligne) : 
    #     print("ok")
    # else :
    #     print("error")  
        
group = lambda liste, size : [liste[i:i+size] for i in range(0, len(liste), size)]

polarity_par_paquet = group(polarity,100)

liste_moyennes = []
for l in polarity_par_paquet :
  liste_moyennes.append(np.mean(l))

plt.plot(liste_moyennes)