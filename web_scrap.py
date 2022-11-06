from base64 import encode
from dataclasses import replace
from urllib.request import Request
import pandas as pd
from csv import writer
import requests
from bs4 import BeautifulSoup

# demande d information à l'utilisateur  
hashtag = input('Entrez votre hashtag: ')
data_size = int(input('Entrez le nombre de tweets: '))


# Remplacez l'url par un autre de votre choix 
url = 'https://www.amazon.fr/Apple-iPhone-14-128-Go/product-reviews/B0BDJH7J5C/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2'

# request get 
r = requests.get(url)

# Utilisation de beautiful soup 
soup = BeautifulSoup(r.content, 'html.parser')

# mettez le bloc qui contient le commentaire que vous voulez extraire 
comment = soup.find_all("span", class_="a-size-base review-text review-text-content")

# print(comment)

# Initialisation d'un tableau de données 
comments = []

# Enregistrement des données 
for i, tweets in enumerate(comment):
    if i > data_size:
        break
    # tweet_data.append([tweets.date, tweets.content, tweets.user.username, tweets.url]) 
    comments.append([tweets.text.strip()]) 

# Enregistrment dans un fichier CSV
df = pd.DataFrame(comments, columns=['Comments'])
df.to_csv(f'{hashtag}.csv', index=False, encoding='utf-8')
