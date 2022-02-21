#--------- VIEWS NETWEETS GAME -----------------#

#Test GitHub

#IMPORTS
import json
from tkinter.ttk import Separator
from django.http import JsonResponse


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

### --- TEST TABLES WITH COMPTE TWITTER DEJA DEFINI DEPUIS UNE AUTRE PAGE--- ###

#test formulaire# 
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

### --- Glossaire (DashBoard - Glossaire) --- ###
def glossaire(request):
    return render(request, 'game/glossaire.html')

### --- FAQ (DashBoard - FAQ) --- ###
def faq(request):
    return render(request, 'game/faq.html')

### --- Geolocalisation (DashBoard - Geolocalisation) --- ###
def geolocalisation(request, compteTwitter_id):
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    return render(request, 'game/geolocalisation.html', locals())

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

### --- Analyse2 (DashBoard - Index) --- ###
def analyse2(request, compteTwitter_id):

    Dict={}
    Dict['compteTwitter']=compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)
    
    #WIDGET CHART PIE (chart-pie-demo.js)
    ratioFollowers = Dict['compteTwitter'].nb_followers/(Dict['compteTwitter'].nb_friends+Dict['compteTwitter'].nb_followers)
    ratioFollowersPourcentage = round(ratioFollowers*100)
    ratioFriendsPourcentage = 100-ratioFollowersPourcentage
    data=[ratioFollowersPourcentage, ratioFriendsPourcentage] #A remplacer par les valeurs calculées voulues (ex : repartition RT/Tweets)
    data=json.dumps(data)

    #WIDGET CHART AREA (chart-area-demo.js)
    labels=[]

    #Objet Label
    firstTweet=Dict['compteTwitter'].tweet_set.order_by('created_at')[0]
    lastTweet=Dict['compteTwitter'].tweet_set.order_by('-created_at')[0] #tweet le plus ancien
    monthFirstTweet=firstTweet.created_at.month
    yearFirstTweet=firstTweet.created_at.year
    monthLastTweet=lastTweet.created_at.month
    yearLastTweet=lastTweet.created_at.year

    i=True


    month=monthFirstTweet
    year=yearFirstTweet

    while i==True : #Première année
        while month < 13 :
            labels.append([month,year]) #A changer pour que ca donne Month/Year[2:4]
            month=month+1
        i=False
        month=0
        year=year+1
    
    while year<yearLastTweet : #Années du milieu
        while month<12 :
            month=month+1
            labels.append([month,year])
        month=0
        year=year+1

    while month < monthLastTweet : 
        month=month+1
        labels.append([month,year])


    
    
    
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

    #WIDGET PROJECTS (barres horizontales)
    nbTweetsRt=0
    nbTweetsWithoutRt=0
    for tweet in Dict['compteTwitter'].tweet_set.all() :
        if "RT" in tweet.text : 
            nbTweetsRt=nbTweetsRt+1
        else :
            nbTweetsWithoutRt=nbTweetsWithoutRt+1
    
    ratioTweetsRt=nbTweetsRt/(nbTweetsRt+nbTweetsWithoutRt)
    ratioTweetsRtPourcentage = round(ratioTweetsRt*100)

    #WIDGET BEST TWEET (barres horizontales)
    popularTweet_nb_like=Dict['compteTwitter'].tweet_set.order_by('-nb_like')[0]


    

    return render(request, 'game/analyse2.html', locals())




#WIDGET EXPORT XL
def export_csv(request, compteTwitter_id):
    pdb.set_trace()
    Dict={}
    Dict['compteTwitter'] = compteTwitter.objects.get(id_compteTwitter=compteTwitter_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export-datas.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Username','Tweet text', 'Nombre de retweet', 'Nombre de likes', 'Nombre de citations', 'Nombre de réponses','Date de création','Langue'])

    tweetsToExport = Dict['compteTwitter'].tweet_set.all()
    for tweet in tweetsToExport:
        row=[Dict['compteTwitter'].username, tweet.text,tweet.nb_rt,tweet.nb_like,tweet.nb_quote,tweet.nb_reply,tweet.created_at,tweet.lang]
        writer.writerow(row)

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
