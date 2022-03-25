#--------- VIEWS NETWEETS GAME -----------------#

#IMPORTS
import json
from tkinter import E
from tkinter.ttk import Separator
from django.http import JsonResponse
from importlib_metadata import _top_level_declared


from .forms import *


import pdb
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netweets.settings")
from django.shortcuts import render
from django.http import HttpResponse
import tweepy
from game.models import *
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


### --- USER ACCOUNT --- ###
def login_html(request):
	try : 
		email = request.POST['inputEmail']
		password = request.POST['inputPassword']
		user=authenticate(email=email,password=password)
	except : 
		return render (request, 'game/login.html')
	
	
    
def register(request):
    return render(request, 'game/register.html')

### --- TEST NEW FORMULAIRE--- ###

def formulaire2(request):
    
    Dict={}
    lastCompteTwitterScraped = compteTwitter.objects.all().order_by('-last_scrap')[0]
    
    form = FormulaireForm(request.POST or None)
    
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        username = form.cleaned_data['name']
        # Nous pourrions ici envoyer l'e-mail grâce aux données
        # que nous venons de récupérer
        envoi = True
        print(username)
        try :
            datas=analyse(username)
            Dict['message']=datas[0]
            Dict['compteTwitter']=datas[1]
            Dict['popularTweet_nb_like']=datas[2]
            Dict['popularTweet_nb_rt']=datas[3]
            Dict['liste_tweets']=[]
            a=tweet.objects.filter(compteTwitter_id=datas[1].id)
            Dict['liste_tweets']=a
        except:
            pass

    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'game/formulaire2.html', locals())

#progress_bar


#formulaire# 
def formulaire(request):
    
    Dict={}
    
    form = FormulaireForm(request.POST or None)
    
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        username = form.cleaned_data['name']
        # Nous pourrions ici envoyer l'e-mail grâce aux données
        # que nous venons de récupérer
        envoi = True
        print(username)
        try :
            datas=analyse(username)
            Dict['message']=datas[0]
            Dict['compteTwitter']=datas[1]
            Dict['popularTweet_nb_like']=datas[2]
            Dict['popularTweet_nb_rt']=datas[3]
            Dict['liste_tweets']=[]
            a=tweet.objects.filter(compteTwitter_id=datas[1].id)
            Dict['liste_tweets']=a
        except:
            pass

    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'game/formulaire.html', locals())

    
### --- TEMPLATES DASHBOARD --- ###

#Fonction pourcentage utilisée dans l'analyse sentimentale
def percentage(part,whole):
    return 100 * float(part)/float(whole)

### --- sentimental (DashBoard - Analyse sentimentale) --- ###
def sentimental(request, compteTwitter_id):
    
    print("Début analyse sentimentale")
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    
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
        
    '''

    #NEW - Analyse sentimentale
    #1 - Construction liste des Tweets
    for tweet in Dict['compteTwitter'].tweet_set.all():
        print(tweet)
        tweet_list.append(tweet.text)
    #2 - Clean liste des tweets
    #2.1 - Suppression doublons
    tweet_list.drop_duplicates(inplace = True)
    #2.2 - Creation nouveau DataFrame
    tw_list = pd.DataFrame(tweet_list)
    tw_list['text'] = tw_list[0]
    #2.3 - Clean RT, Punctuation etc
    remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
    rt = lambda x: re.sub("(@[A-Za-z0–9]+)|([⁰-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] = tw_list.text.str.lower()
    tw_list.head(10)
    pdb.set_trace()
    '''




    return render(request, 'game/sentimental.html', locals())


### --- Roadmap (DashBoard - Glossaire) --- ###
def roadmap(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    #WIDGET BEST TWEET (barres horizontales)
    print('Debut Widget Best Tweets')
    bestTweet_id=Dict['compteTwitter'].tweet_set.order_by('-nb_like')[0].id_tweet
    popularTweet_nb_like=Dict['compteTwitter'].tweet_set.order_by('-nb_like')[0].id_tweet
    popularTweet_nb_rt=Dict['compteTwitter'].tweet_set.order_by('-nb_rt')[0].id_tweet
    popularTweet_nb_quote=Dict['compteTwitter'].tweet_set.order_by('-nb_quote')[0].id_tweet
    popularTweet_nb_reply=Dict['compteTwitter'].tweet_set.order_by('-nb_reply')[0].id_tweet
    print('END Widget Best Tweets')


    #WIDGET Encarts top
    #Object Nombre Moyen Retweets par Tweet
    print('Debut Widgets Encarts TOP')
    dateFirstTweet = Dict['compteTwitter'].tweet_set.order_by('created_at')[0].created_at
    dateLastTweet = Dict['compteTwitter'].tweet_set.order_by('-created_at')[0].created_at
    dateFirstTweet = format_datetime(dateFirstTweet, locale='fr')
    dateLastTweet = format_datetime(dateLastTweet, locale='fr')



    nbRetweetsTotal=0
    nbTweetsTotal=0
    for tweet in Dict['compteTwitter'].tweet_set.all() :
        nbRetweetsTotal=nbRetweetsTotal+tweet.nb_rt
        nbTweetsTotal=nbTweetsTotal+1
    nbRetweetsMoyenParTweet=nbRetweetsTotal/nbTweetsTotal
    nbRetweetsMoyenParTweet=round(nbRetweetsMoyenParTweet,2)
    print('END Widgets Encarts TOP')


    #WIDGET CHART AREA (chart-area-demo.js)
    print('Debut Widget Chart Area')

    #Sous widget - Nombre Tweets / Mois -
    #Objet Label
    labels = buildLabels(Dict['compteTwitter'].tweet_set.order_by('created_at')[0].created_at, Dict['compteTwitter'].tweet_set.order_by('-created_at')[0].created_at )

    
    
    #Objet général DictionnaireDatas
    Dict['datas']={}
    for date in labels : 
        Dict['datas'][date[0],date[1]]=0

    #Objet nbTweetsPerMonth
    nbTweetsPerMonth=[]
    for tweet in Dict['compteTwitter'].tweet_set.all():
        for date in labels :
            if tweet.created_at.month == date[0] and tweet.created_at.year == date[1] :
                Dict['datas'][date[0],date[1]]= Dict['datas'][date[0],date[1]]+1
            else:
                pass

    #Construction de nbTweetsPerMonth
    nbTweetsPerMonth=[]
    for key in Dict['datas'].keys() :
        nbTweetsPerMonth.append(Dict['datas'][key])
    
    #Objet ratioLikesPerTweetPerMonth
    ratioLikesPerTweetPerMonth = []
    for date in labels : 
        nbLikesPerMonth = 0
        for tweet in Dict['compteTwitter'].tweet_set.all():
            if tweet.created_at.month == date[0] and tweet.created_at.year == date[1] :
                nbLikesPerMonth=nbLikesPerMonth+tweet.nb_like
        if Dict['datas'][date[0],date[1]] != 0 : #Condition pour éviter la division par 0
            ratioLikesPerTweet = round(nbLikesPerMonth/Dict['datas'][date[0],date[1]], 2)
        else : 
            ratioLikesPerTweet = 0
        ratioLikesPerTweetPerMonth.append(ratioLikesPerTweet)

    
    #Objet ratioRTPerTweetPerMonth
    ratioRTPerTweetPerMonth = []
    for date in labels : 
        nbRTPerMonth = 0
        for tweet in Dict['compteTwitter'].tweet_set.all():
            if tweet.created_at.month == date[0] and tweet.created_at.year == date[1] :
                nbRTPerMonth=nbRTPerMonth+tweet.nb_rt
        if Dict['datas'][date[0],date[1]] != 0 : #Condition pour éviter la division par 0
            ratioRTPerTweet = round(nbRTPerMonth/Dict['datas'][date[0],date[1]], 2)
        else : 
            ratioRTPerTweet = 0
        ratioRTPerTweetPerMonth.append(ratioRTPerTweet)


                


    #Verif recup totalité des tweets
    compteur=0
    nbTweetsObject = len(Dict['compteTwitter'].tweet_set.all())
    for key in Dict['datas'].keys() :
        compteur=compteur+Dict['datas'][key]
    print('Nombre total de Tweets recupérés initialement : ', nbTweetsObject)
    print('Nombre total de Tweets poussés dans le widget Chart Area : ', compteur)
    print('Liste des tweets : ', nbTweetsPerMonth)

    
    #Rework to send to JS
    labelsClean=[]
    for elem in labels :
        elemClean=str(elem[0])+'/'+str(elem[1])
        labelsClean.append(elemClean)
    labelsClean = json.dumps(labelsClean)
    print('END Widget Chart Area')



    return render(request, 'game/roadmap.html', locals())


### --- Glossaire (DashBoard - Glossaire) --- ###
def glossaire(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    listeTweets=[]
    return render(request, 'game/glossaire.html', locals())

### --- FAQ (DashBoard - FAQ) --- ###
def faq(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    return render(request, 'game/faq.html', locals())

### --- Geolocalisation (DashBoard - Geolocalisation) --- ###
def geolocalisation(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    return render(request, 'game/geolocalisation.html', locals())

### --- Nuage de mots (DashBoard - Nuage de points - WordCloud) --- ###
def create_wordcloud(text):
    #mask = np.array(Image.open('cloud.png'))
    stopwords = list(fr_stop)
    wc = WordCloud(background_color='white',
    # mask = mask,
    max_words=3000,
    stopwords=stopwords,
    repeat=False)
    wc.generate(str(text))
    wc.to_file('game/static/game/wordcloud/wc.png')
    print('Word Cloud Saved Successfully')
    path='game/static/game/wordcloud/wc.png'
    # display(Image.open(path))

def nuage(request, compteTwitter_id):
    print('--- START Fonction WordCloud ---')
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    liste_tweets = []
    for tweet in Dict['compteTwitter'].tweet_set.all() :
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
    #Creating wordcloud for all tweets
    listeCleanFinale = []
    for text in tw_listClean["text"] :
        listeCleanFinale.append(text)
    create_wordcloud(listeCleanFinale)
    print('--- END Fonction WordCloud ---')

    return render(request, 'game/nuage.html', locals())

### --- Reports (DashBoard - Reports) --- ###
def reports(request, compteTwitter_id): 
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    return render(request, 'game/reports.html', locals())

### --- Tables --- ###
def tables(request, compteTwitter_id): #On demande l'ID du compteTwitter pour appelé le DB avec les datas correspondantes
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    return render(request, 'game/tables.html', locals())

###--- Fonction construction labels ---###
def buildLabels(firstDate, lastDate):
    labels=[]
    n=1
    while firstDate.month != lastDate.month or firstDate.year != lastDate.year :
        labels.append([firstDate.month, firstDate.year])
        firstDate = firstDate + relativedelta(months=n)
    labels.append([lastDate.month, lastDate.year])
    return (labels)


### --- Analyse2 (DashBoard - Index) --- ###
def analyse2(request, compteTwitter_id):
    print('# ------- Fonction ANALYSE2.. ------- #')
    Dict={}
    Dict['compteTwitter']=compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    #Objet période d'analyse
    dateFirstTweet = Dict['compteTwitter'].tweet_set.order_by('created_at')[0].created_at
    dateLastTweet = Dict['compteTwitter'].tweet_set.order_by('-created_at')[0].created_at
    dateFirstTweet = format_datetime(dateFirstTweet, locale='fr')
    dateLastTweet = format_datetime(dateLastTweet, locale='fr')


    #WIDGET Encarts top
    #Object Nombre Moyen Retweets par Tweet
    print('Debut Widgets Encarts TOP')

    nbRetweetsTotal=0
    nbTweetsTotal=0
    for tweet in Dict['compteTwitter'].tweet_set.all() :
        nbRetweetsTotal=nbRetweetsTotal+tweet.nb_rt
        nbTweetsTotal=nbTweetsTotal+1
    nbRetweetsMoyenParTweet=nbRetweetsTotal/nbTweetsTotal
    nbRetweetsMoyenParTweet=round(nbRetweetsMoyenParTweet,2)
    print('END Widgets Encarts TOP')

    #WIDGET CHART PIE (chart-pie-demo.js)
    print('Debut Widgets Chart Pie')
    if Dict['compteTwitter'].nb_friends == 0 or Dict['compteTwitter'].nb_followers == 0 : 
        ratioFollowersPourcentage = 50
        ratioFriendsPourcentage = 50
    else :
        ratioFollowers = Dict['compteTwitter'].nb_followers/(Dict['compteTwitter'].nb_friends+Dict['compteTwitter'].nb_followers)
        ratioFollowersPourcentage = round((ratioFollowers*100), 2)
        ratioFriendsPourcentage = round(100-ratioFollowersPourcentage, 2)
    data=[ratioFollowersPourcentage, ratioFriendsPourcentage] #A remplacer par les valeurs calculées voulues (ex : repartition RT/Tweets)
    data=json.dumps(data)
    print('END Widgets Chart Pie')


    #WIDGET CHART AREA (chart-area-demo.js)
    print('Debut Widget Chart Area')

    #Sous widget - Nombre Tweets / Mois -
    #Objet Label
    labels = buildLabels(Dict['compteTwitter'].tweet_set.order_by('created_at')[0].created_at, Dict['compteTwitter'].tweet_set.order_by('-created_at')[0].created_at )

    
    
    #Objet général DictionnaireDatas
    Dict['datas']={}
    for date in labels : 
        Dict['datas'][date[0],date[1]]=0

    #Objet nbTweetsPerMonth
    nbTweetsPerMonth=[]
    for tweet in Dict['compteTwitter'].tweet_set.all():
        for date in labels :
            if tweet.created_at.month == date[0] and tweet.created_at.year == date[1] :
                Dict['datas'][date[0],date[1]]= Dict['datas'][date[0],date[1]]+1
            else:
                pass

    #Construction de nbTweetsPerMonth
    nbTweetsPerMonth=[]
    for key in Dict['datas'].keys() :
        nbTweetsPerMonth.append(Dict['datas'][key])
    
    #Objet ratioLikesPerTweetPerMonth
    ratioLikesPerTweetPerMonth = []
    for date in labels : 
        nbLikesPerMonth = 0
        for tweet in Dict['compteTwitter'].tweet_set.all():
            if tweet.created_at.month == date[0] and tweet.created_at.year == date[1] :
                nbLikesPerMonth=nbLikesPerMonth+tweet.nb_like
        if Dict['datas'][date[0],date[1]] != 0 : #Condition pour éviter la division par 0
            ratioLikesPerTweet = round(nbLikesPerMonth/Dict['datas'][date[0],date[1]], 2)
        else : 
            ratioLikesPerTweet = 0
        ratioLikesPerTweetPerMonth.append(ratioLikesPerTweet)

    
    #Objet ratioRTPerTweetPerMonth
    ratioRTPerTweetPerMonth = []
    for date in labels : 
        nbRTPerMonth = 0
        for tweet in Dict['compteTwitter'].tweet_set.all():
            if tweet.created_at.month == date[0] and tweet.created_at.year == date[1] :
                nbRTPerMonth=nbRTPerMonth+tweet.nb_rt
        if Dict['datas'][date[0],date[1]] != 0 : #Condition pour éviter la division par 0
            ratioRTPerTweet = round(nbRTPerMonth/Dict['datas'][date[0],date[1]], 2)
        else : 
            ratioRTPerTweet = 0
        ratioRTPerTweetPerMonth.append(ratioRTPerTweet)


                


    #Verif recup totalité des tweets
    compteur=0
    nbTweetsObject = len(Dict['compteTwitter'].tweet_set.all())
    for key in Dict['datas'].keys() :
        compteur=compteur+Dict['datas'][key]
    print('Nombre total de Tweets recupérés initialement : ', nbTweetsObject)
    print('Nombre total de Tweets poussés dans le widget Chart Area : ', compteur)
    print('Liste des tweets : ', nbTweetsPerMonth)

    
    #Rework to send to JS
    labelsClean=[]
    for elem in labels :
        elemClean=str(elem[0])+'/'+str(elem[1])
        labelsClean.append(elemClean)
    labelsClean = json.dumps(labelsClean)
    print('END Widget Chart Area')


    #WIDGET PROJECTS (=Statstiques -> barres horizontales)
    #Object Retweets Ratio
    print('Debut RT Ratio')

    nbTweetsRt=0
    nbTweetsWithoutRt=0
    for tweet in Dict['compteTwitter'].tweet_set.all() :
        if "RT" in tweet.text : 
            nbTweetsRt=nbTweetsRt+1
        else :
            nbTweetsWithoutRt=nbTweetsWithoutRt+1
    
    ratioTweetsRt=nbTweetsRt/(nbTweetsRt+nbTweetsWithoutRt)
    ratioTweetsRtPourcentage = round(ratioTweetsRt*100, 2)

    #Object Retweets Ratio
    nbTweetsRt=0
    nbTweetsWithoutRt=0
    for tweet in Dict['compteTwitter'].tweet_set.all() :
        if "RT" in tweet.text : 
            nbTweetsRt=nbTweetsRt+1
        else :
            nbTweetsWithoutRt=nbTweetsWithoutRt+1
    
    ratioTweetsRt=nbTweetsRt/(nbTweetsRt+nbTweetsWithoutRt)
    ratioTweetsRtPourcentage = round(ratioTweetsRt*100, 2)
    print('END RT Ratio')


    #Object Tweets avec Hashtag
    print('Debut Tweets avec Hashtag')

    nbTweetsHashtag=0
    for tweet in Dict['compteTwitter'].tweet_set.all() :
        if "#" in tweet.text :
            nbTweetsHashtag=nbTweetsHashtag+1
    ratioNbTweetsHashtag = nbTweetsHashtag / len(Dict['compteTwitter'].tweet_set.all())
    ratioNbTweetsHashtagPourcentage = round (ratioNbTweetsHashtag*100, 2)
    print('END Tweets avec Hashtag')

    
    #Object RatioDaysWithTweet
    print('Debut Ratio Days With Tweets')
    RatioDaysWithTweet = 0
    nbDays = 0
    nbDaysWithTweet = 0
    i = -1
    dateCreationCompte = Dict['compteTwitter'].created_at.replace(tzinfo=None) #Formatage necessaire pour permettre la soustraction de datetime.time 
    nbDays = datetime.now() - dateCreationCompte
    nbDays = nbDays.days

    for tweet in Dict['compteTwitter'].tweet_set.order_by('-created_at') : #combien de day différent avec un tweet ?
        try : #Permet de prendre en compte le premier Tweet
            if tweet.created_at.day != Dict['compteTwitter'].tweet_set[i].created_at.day or tweet.created_at.month != Dict['compteTwitter'].tweet_set[i].created_at.month or tweet.created_at.year !=  Dict['compteTwitter'].tweet_set[i].created_at.year :
                nbDaysWithTweet += 1  
            else : 
                pass
            
            i=i+1
        except : 
            nbDaysWithTweet = nbDaysWithTweet +1 #Cas du premier tweet
            i=i+1
            continue
    ratioDaysWithTweet = round((nbDaysWithTweet/nbDays)*100, 2)
    print('Fin Ratio Days With Tweets')

            



    #WIDGET BEST TWEET (barres horizontales)
    print('Debut Widget Best Tweets')
    bestTweet_id=Dict['compteTwitter'].tweet_set.order_by('-nb_like')[0].id_tweet
    popularTweet_nb_like=Dict['compteTwitter'].tweet_set.order_by('-nb_like')[0].id_tweet
    popularTweet_nb_rt=Dict['compteTwitter'].tweet_set.order_by('-nb_rt')[0].id_tweet
    popularTweet_nb_quote=Dict['compteTwitter'].tweet_set.order_by('-nb_quote')[0].id_tweet
    popularTweet_nb_reply=Dict['compteTwitter'].tweet_set.order_by('-nb_reply')[0].id_tweet
    print('END Widget Best Tweets')




    
    print('# ------- END Fonction ANALYSE2.. ------- #')
    return render(request, 'game/analyse2.html', locals())




#WIDGETS EXPORT XL par Module
def analyse2_export_csv(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export-datas.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Username','Tweet text', 'Nombre de retweet', 'Nombre de likes', 'Nombre de citations', 'Nombre de réponses','Date de création','Langue'])

    tweetsToExport = Dict['compteTwitter'].tweet_set.all()
    for tweet in tweetsToExport:
        row=[Dict['compteTwitter'].username, tweet.text.encode('ascii','ignore'),tweet.nb_rt,tweet.nb_like,tweet.nb_quote,tweet.nb_reply,tweet.created_at,tweet.lang]
        writer.writerow(row)
    return(response)

def sentimental_export_csv(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export-datas.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Username','Tweet text', 'Sentiment', 'Nombre de retweet', 'Nombre de likes', 'Nombre de citations', 'Nombre de réponses','Date de création','Langue'])

    print("Début analyse sentimentale")
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    
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
            etat = "Negatif"
        elif pos > neg:
            positive_list.append(tweet_text)
            positive += 1
            etat = "Positif"

        elif pos == neg:
            neutral_list.append(tweet_text)
            neutral += 1
            etat = "Neutre"


        row=[Dict['compteTwitter'].username, tweet.text.encode('ascii','ignore'), etat, tweet.nb_rt,tweet.nb_like,tweet.nb_quote,tweet.nb_reply,tweet.created_at,tweet.lang]
        writer.writerow(row)

    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)
    polarity = percentage(polarity, noOfTweet)
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')
    return(response)


#WIDGET PROJECTS (barres horizontales)
    

    return response
### --- ANALYSE --- ###
def analyse(username):
    ##FONCTION AU CLICK
    try : 
        compte = compteTwitter.objects.get(username=username)
        message="Le compte Twitter existe déjà dans la base de données..."
        #Update de la BDD
        try:
            update(username)
        except:
            print('-- WARNING -- :  problème dans la fonction upadate()')
            pass
    except : 
        message="Le compte Twitter existe PAS dans la BDD, scrapping lancé..."
        scrap(username)
        compte = compteTwitter.objects.get(username=username)
        pass
    print(message)
    popularTweet_nb_like=compte.tweet_set.order_by('-nb_like')[0] #relation inverse ForeignKey : ajouter _set à la suite de l'objet lié appelé.
    popularTweet_nb_rt=compte.tweet_set.order_by('-nb_rt')[0] #relation inverse ForeignKey : ajouter _set à la suite de l'objet lié appelé.
    return(message, compte, popularTweet_nb_like, popularTweet_nb_rt)
 
def update(username):
    
    print('# ------- Fonction UPDATE.. ------- #')
    
    # API KEYS #
    api = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAEH0WQEAAAAAiqnTtZBRAfML3KmKSWCcxzCE0uo%3DjXMKdzyR46LRPnn7nkIjkjoBDBfcDaraQ4V7k7yrJvHGatAz0i",
    consumer_key="8dGv0kBU1xEm5PfI2doTNeIg1", consumer_secret="vid6ftopGorCriqduh8b26PCHgQlaqN7AvdVngc3sKnnFdUPGg",
    access_token="1111590746560307200-DrqgzEleaKB0AVIT7QJ1wAo5M70wRR",
    access_token_secret="Xsf841vMDbqkko3MmUe0RSPHioQHlXJR8GmG4jNZsCsye", wait_on_rate_limit=True)
    # GET GENERAL INFO #
    compte = compteTwitter.objects.get(username=username)
    last_tweet_scraped = compte.tweet_set.order_by('-created_at')[0]
    user_information=api.get_user(username=username, user_fields=['created_at','description','profile_image_url','public_metrics'])
    
    #Test nouveaux Tweets ? >0
    last_tweet_tweeted = api.get_users_tweets(compte.id_compteTwitter,max_results=10,since_id=last_tweet_scraped.id_tweet,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
    if last_tweet_tweeted.meta['result_count']>0 :
        
        
        print('# ------- Nouveaux Tweets, on UPDATE la BDD.. ------- #')
        #Comparaison infos générales et update : 
        if compte.name != user_information.data.name :
            compte.name=user_information.data.name
        if compte.description != user_information.data.description :
            compte.description=user_information.data.description
        if compte.nb_followers != user_information.data.public_metrics['followers_count'] :
            compte.nb_followers=user_information.data.public_metrics['followers_count']
        if compte.nb_friends != user_information.data.public_metrics['following_count'] :
            compte.nb_friends = user_information.data.public_metrics['following_count']
        if compte.nb_tweets != user_information.data.public_metrics['tweet_count'] :
            compte.nb_tweets= user_information.data.public_metrics['tweet_count']
        if compte.nb_listed != user_information.data.public_metrics['listed_count'] :
            compte.nb_listed = user_information.data.public_metrics['listed_count']
        if compte.profile_image_url != user_information.data.profile_image_url :
            compte.profile_image_url = user_information.data.profile_image_url
        
        
        #Scrap des nouveaux Tweets et enregistrement..
        #1er enregistrement..
        last_tweets_tweeted = api.get_users_tweets(compte.id_compteTwitter,max_results=100,since_id=last_tweet_scraped.id_tweet,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
        #Boucle enregistrement des nouveaux Tweets dans la BDD
        for t in last_tweets_tweeted.data :
            id_tweet = t.id
            nb_rt=t.public_metrics['retweet_count'] #nb_retweet
            nb_reply=t.public_metrics['reply_count'] #nb_reply
            nb_like=t.public_metrics['like_count'] #nb_like
            nb_quote=t.public_metrics['quote_count'] #nb_quote
            text=t.text #text
            created_at=t.created_at #date de création du tweet
            lang=t.lang #langue du tweet
            
            #Creation objet + enregistrement (tweet)
            t2 = tweet(id_tweet=id_tweet, text=text, nb_rt=nb_rt, nb_reply=nb_reply, nb_like=nb_like, nb_quote=nb_quote, 
            created_at=created_at,lang=lang, compteTwitter=compte)
            t2.save()

        #2eme enreigstrement BOUCLE, since_id = compte.tweet_set.order_by('-created_at')[0]
        while last_tweets_tweeted.meta['result_count'] > 0 : 
            last_tweet_scraped = compte.tweet_set.order_by('-created_at')[0]
            last_tweets_tweeted = api.get_users_tweets(compte.id_compteTwitter,max_results=100,since_id=last_tweet_scraped.id_tweet,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
            
            try : 
                for t in last_tweets_tweeted.data :
                    id_tweet = t.id
                    nb_rt=t.public_metrics['retweet_count'] #nb_retweet
                    nb_reply=t.public_metrics['reply_count'] #nb_reply
                    nb_like=t.public_metrics['like_count'] #nb_like
                    nb_quote=t.public_metrics['quote_count'] #nb_quote
                    text=t.text #text
                    created_at=t.created_at #date de création du tweet
                    lang=t.lang #langue du tweet
                    
                    #Creation objet + enregistrement (tweet)
                    t2 = tweet(id_tweet=id_tweet, text=text, nb_rt=nb_rt, nb_reply=nb_reply, nb_like=nb_like, nb_quote=nb_quote, 
                    created_at=created_at,lang=lang, compteTwitter=compte)
                    t2.save()
            except :
                pass
        
        #Update last_scrap :
        compte.last_scrap=datetime.now()
        compte.save()
        
        print('UPDATE TERMINE')
         
def maj(request):
    return render(request, 'game/maj.html')
    
def accueil(request):
    cs = compteTwitter.objects.all()
    c = random.choice(cs)
    return render(request, 'game/accueil.html', {'compte_twitter': c})

### --- GAME --- ###

def gameClick(request):
    IDgame = request.GET['IDgame']
    IDcompteClick = int(IDgame.split(',')[1])
    IDjeu = int(IDgame.split(',')[0])
    resultat=resultatJeu(IDcompteClick, IDjeu)
    #return JsonResponse({"resultat": resultat}) #Pas le bon retour
    return render(request, 'game/game.html', locals()) #Comment retourner les données à la page ? sans actualisation

def resultatJeu(IDcompteClick, IDjeu):
    print('fonction resultatJeu')
    game = jeu.objects.all().filter(id=IDjeu)
    if game[0].win_id == (IDcompteClick) :
        print('Gagné !')
        resultat='WIN'
    else : 
        print('Perdu !')
        resultat='LOOSE'
        
    return(resultat)
    
    
def game(request):
    
    #Dictionnaire
    datas = {}
    datas['c1']={}
    datas['c2']={}
    
    #Tweet au hasard et compte associé
    tweets = tweet.objects.all()
    t = random.choice(tweets)
    
    #Compte au hasard
    comptes = compteTwitter.objects.all()
    c = random.choice(comptes)
    
    #Verif que le compte du tweet != du compte récupéré
    while c.username == t.compteTwitter.username :
        c = random.choice(comptes)
      
        
    #Verif que le created_at du tweet est < au created_at du compte twitter de comparaison
        
    #Construction dictionnaire datas    
    datas = {}
    datas['c1']={}
    datas['c2']={}
    datas['tweet']=t
    #Randomize dictionnaire
    liste = ['c1','c2']
    l=random.choice(liste)
    datas[l]['tweet']=t
    datas[l]['compteTwitter']=t.compteTwitter
    datas[l]['win']=True
    for elem in liste : 
        if elem != l :
            datas[elem]['compteTwitter']=c
            datas[elem]['win']=False
    #Creation objet game :
    jeux=jeu(compteTwitter1=datas['c1']['compteTwitter'], compteTwitter2=datas['c2']['compteTwitter'],win=t.compteTwitter, tweet=datas['tweet'])
     
    jeux.save()   
    return render(request, 'game/game.html', {'jeux': jeux})    


# Create your views here.
def scrap(username):
    
    print('# ------- Fonction SCRAP 0.1.. ------- #')
    #Variables globales :
    bolScrap=True
    #Date du jour
    #bolScrap = True : on scrap et on met False si ca existe deja

    #API KEYS + AUTH
    api = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAEH0WQEAAAAAiqnTtZBRAfML3KmKSWCcxzCE0uo%3DjXMKdzyR46LRPnn7nkIjkjoBDBfcDaraQ4V7k7yrJvHGatAz0i",
    consumer_key="8dGv0kBU1xEm5PfI2doTNeIg1", consumer_secret="vid6ftopGorCriqduh8b26PCHgQlaqN7AvdVngc3sKnnFdUPGg",
    access_token="1111590746560307200-DrqgzEleaKB0AVIT7QJ1wAo5M70wRR",
    access_token_secret="Xsf841vMDbqkko3MmUe0RSPHioQHlXJR8GmG4jNZsCsye", wait_on_rate_limit=True) #wait_on_rate_limit à changer en TRUE pour continuer le scrapping ? 

    #GET GENERAL INFO
    user_information=api.get_user(username=username)

    #ETAPE 1 : scrap compte twitter + create object compteTwitter
        #A - Le compte Twitter existe il déjà dans la BDD   
    try :
        for c in compteTwitter.objects.all() :

            if c.username == username :
                        #a - OUI

                print('Le compte existe déjà dans la BDD')
                #De quand date le dernier scraping ?
                print ('Date du dernier scrapping : ', c.created_at)
                #Comparaison date du jour / date du dernier scrapping
                #Si récent : bolScrap = False. --> Conditions : compte existe, et scrappé recemment : bolScrap = False
                bolScrap = False

            else :
                continue

    except :
        print('Problème...')
        print('username', username)
        pass

    if bolScrap == True :
        print('Le compte existe PAS dans la BDD : lancement du scrapping..')
        print('Enregistrement du compte Twitter...')
        user_information=api.get_user(username=username, user_fields=['created_at','description','profile_image_url','public_metrics'])
        
        id_compteTwitter = user_information.data.id #ID
        name = user_information.data.name #name 
        username = user_information.data.username #username (=screen_name sans le @)
        created_at=user_information.data.created_at #date de création du compte
        description=user_information.data.description #description
        profile_image_url=user_information.data.profile_image_url #URL image profil
        profile_url= "https://twitter.com/" + username
        nb_followers=user_information.data.public_metrics['followers_count'] #Nombre de followers
        nb_friends=user_information.data.public_metrics['following_count'] #Nombre de following
        nb_tweets=user_information.data.public_metrics['tweet_count'] #Nombre de tweets
        nb_listed=user_information.data.public_metrics['listed_count'] # ??? 
        
        last_scrap=datetime.now() #date du moment
         
        
        #Creation objet + enregistrement (compteTwitter)
        c = compteTwitter(id_compteTwitter=id_compteTwitter, name=name, username=username, created_at=created_at, 
        profile_image_url = profile_image_url, nb_followers=nb_followers, nb_friends=nb_friends, nb_tweets=nb_tweets, nb_listed=nb_listed, last_scrap=last_scrap, description=description, profile_url = profile_url  )
        c.save()
        print('Enregistrement des tweets...')
        
        
        # ENREGISTREMENT TWEETS # -> à vérfiier, prend ne compte les replies mais doit exclure d'autres tweets 
        # A VERIFIER PAR RAPPORT A NINOCLEVA
        #Enregistrement de la première liste de tweets
        liste_tweets = api.get_users_tweets(user_information.data.id,max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
        for t in liste_tweets.data :
            #cas des RT à prévoir : reply/like/quote sur le retweet (=tweet du compte étudié), le nb_RT concerne le tweet initial
            id_tweet = t.id
            nb_rt=t.public_metrics['retweet_count'] #nb_retweet
            nb_reply=t.public_metrics['reply_count'] #nb_reply
            nb_like=t.public_metrics['like_count'] #nb_like
            nb_quote=t.public_metrics['quote_count'] #nb_quote
            text=t.text #text
            created_at=t.created_at #date de création du tweet
            lang=t.lang #langue du tweet
            
            #Creation objet + enregistrement (tweet)
            t2 = tweet(id_tweet=id_tweet, text=text, nb_rt=nb_rt, nb_reply=nb_reply, nb_like=nb_like, nb_quote=nb_quote, 
            created_at=created_at,lang=lang, compteTwitter=c)
            t2.save()
        
        #Enregistrement des autres listes
        while liste_tweets.meta['result_count'] > 0 :
            liste_tweets = api.get_users_tweets(user_information.data.id,until_id=liste_tweets.meta['oldest_id'],max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
            try : 
                for t in liste_tweets.data :
                #cas des RT à prévoir : reply/like/quote sur le retweet (=tweet du compte étudié), le nb_RT concerne le tweet initial
                    id_tweet = t.id
                    nb_rt=t.public_metrics['retweet_count'] #nb_retweet
                    nb_reply=t.public_metrics['reply_count'] #nb_reply
                    nb_like=t.public_metrics['like_count'] #nb_like
                    nb_quote=t.public_metrics['quote_count'] #nb_quote
                    text=t.text #text
                    created_at=t.created_at #date de création du tweet
                    lang=t.lang #langue du tweet
                    
                    #Creation objet + enregistrement (tweet)
                    t2 = tweet(id_tweet=id_tweet, text=text, nb_rt=nb_rt, nb_reply=nb_reply, nb_like=nb_like, nb_quote=nb_quote, 
                    created_at=created_at,lang=lang, compteTwitter=c)
                    t2.save()
            except :
                pass
        
        print('Enregistrement terminé.')
            
#######################

