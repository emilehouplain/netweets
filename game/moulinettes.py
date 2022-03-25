# IMPORTS
#--------- VIEWS NETWEETS GAME -----------------#

#IMPORTS
from django.db import models
from datetime import datetime

import json
from tkinter import E
from tkinter.ttk import Separator
from django.http import JsonResponse
from importlib_metadata import _top_level_declared

import pdb
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netweets.settings")
from django.shortcuts import render
from django.http import HttpResponse
import tweepy
from models import *
import random 

import pdb
import tweepy
import pickle
import sys
import networkx as nx
import time

import math
import os
import csv
import folium
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView

import unicodedata

from dateutil.relativedelta import relativedelta
from babel.dates import format_datetime

#IMPORTS : Analyse sentimentale 
from textblob import TextBlob
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('vader_lexicon')
from deep_translator import GoogleTranslator

#Wordcloud
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import re
from nltk.corpus import stopwords
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop

'''
1 - liste compteTwitter candidats
2 - Scrap via formulaire APP des Tweets

- Moulinettes -
4 - Nb mots analysés
5 - Nb mots différents analysés
6 - Nb tweets analysés
7 - Analyse sentimental (via Sentimental APP)
8 - Wordcloud Gloabl (via Nuage APP)
9 - Analyse sentimental Overtime -> fichier excel ?
10 - WordCloud par sentiment  
'''

def AnalyseNumbers(compteTwitter_id) :
    Dict={}
    nbWordsTweet=0
    nbWordsTotal=0
    listWordsTotal=[]
    listeWordsUnique=[]
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    noOfTweet = len(Dict['compteTwitter'].tweet_set.all()) #Nb tweets analysés (6)

    for tweet in Dict['compteTwitter'].tweet_set.all():
        nbWordsTweet = len(tweet.text.split())
        nbWordsTotal = nbWordsTotal + nbWordsTweet
        for mot in tweet.text.split() :
            listWordsTotal.append(mot)
    
    noOfTweet = len(Dict['compteTwitter'].tweet_set.all()) #Nb tweets analysés (6)

    print(noOfTweet) #Nb tweets analysés (6)
    print(nbWordsTotal) #Nb words analysés (4)
    print(len(listWordsTotal)) #Nb words analysés (4)
    listeWordsUnique = set(listWordsTotal)
    print(len(listeWordsUnique)) #Nb words uniques analysés (5)

    #Analyse Sentimental (7)
    #Init vars globales pour analyse sentimentale
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []
    noOfTweet = len(Dict['compteTwitter'].tweet_set.all())

    pdb.set_trace()
    #LEGACY - Analyse sentimentale
    for tweet in Dict['compteTwitter'].tweet_set.all():
        print(tweet)
        tweet_text = GoogleTranslator(source='auto', target='en').translate(tweet.text)

        tweet_list.append(tweet_text)
        analysis = TextBlob(tweet_text)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet_text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity
        
        if neg > pos:
            negative_list.append(tweet_text)
            negative += 1
        elif pos > neg:
            positive_list.append(tweet_text)
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet_text)
            neutral += 1

    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)

    polarity = percentage(polarity, noOfTweet)
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')

    liste_tweets=[]
    for tweet in negative_list :
        liste_tweets.append(tweet.text)
    tw_list = pd.DataFrame(liste_tweets)
    tw_list["text"] = tw_list[0]
    #Clean tweets : RT / username / lowercase
    liste_tweetsClean = []
    for tweet in tw_list["text"] :
        tweet = re.sub(r'@[A-Z0-9a-z_:]+','',tweet)
        tweet = re.sub(r'^[RT]+','',tweet)
        tweet = re.sub('https?://[A-Za-z0-9./]+','',tweet)
        tweet = tweet.lower()
        liste_tweetsClean.append(tweet)
    tw_listClean = pd.DataFrame(liste_tweetsClean)
    tw_listClean["text"] = tw_listClean[0]
    tw_listClean.head(10)

    #Creating wordcloud for all tweets
    #mask = np.array(Image.open('cloud.png'))
    stopwords = list(fr_stop)
    wc = WordCloud(background_color='white',
    # mask = mask,
    max_words=3000,
    stopwords=stopwords,
    repeat=True)
    wc.generate(str(tw_listClean))
    wc.to_file('game/static/game/wordcloud/wc.png')
    print('Word Cloud Saved Successfully')
    path='game/static/game/wordcloud/wc-negative.png'
    # display(Image.open(path))
    print('--- END Fonction WordCloud ---')

AnalyseNumbers(1183418538285027329)










    

