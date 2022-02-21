import pdb
import tweepy
import pickle
import sys
import networkx as nx
import time



username='MonZippo'

api = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAEH0WQEAAAAAiqnTtZBRAfML3KmKSWCcxzCE0uo%3DjXMKdzyR46LRPnn7nkIjkjoBDBfcDaraQ4V7k7yrJvHGatAz0i",
consumer_key="8dGv0kBU1xEm5PfI2doTNeIg1", consumer_secret="vid6ftopGorCriqduh8b26PCHgQlaqN7AvdVngc3sKnnFdUPGg",
access_token="1111590746560307200-DrqgzEleaKB0AVIT7QJ1wAo5M70wRR",
access_token_secret="Xsf841vMDbqkko3MmUe0RSPHioQHlXJR8GmG4jNZsCsye", wait_on_rate_limit=False)

user_information=api.get_user(username=username)

user_information=api.get_user(username=username, user_fields=['created_at','description','profile_image_url','public_metrics'])


############# ALGO ############
liste_tweets = api.get_users_tweets(user_information.data.id,max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
print('Premier tweet recup :', liste_tweets.data[0])
print('Dernier tweet recup :', liste_tweets.data[len(liste_tweets.data)-1])
while liste_tweets.meta['result_count'] > 0 :
	liste_tweets = api.get_users_tweets(user_information.data.id,until_id=liste_tweets.meta['oldest_id'],max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
	print('Premier tweet recup :', liste_tweets.data[0])
	print('Dernier tweet recup :', liste_tweets.data[len(liste_tweets.data)-1])
	
	
liste_tweets = api.get_users_tweets(user_information.data.id,max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
liste_tweets2 = api.get_users_tweets(user_information.data.id,until_id=liste_tweets.meta['oldest_id'],max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets
liste_tweets3 = api.get_users_tweets(user_information.data.id,until_id=liste_tweets2.meta['oldest_id'],max_results=100,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets

pdb.set_trace()

liste_tweets2 = api.get_users_mentions(user_information.data.id,max_results=99,tweet_fields=['author_id','created_at','public_metrics','lang'])#Liste des tweets


liste_tweets3=tweepy.Paginator(api.get_users_tweets, user_information.data.id,max_results=100)
for elem in liste_tweets3 :
	elem.meta['oldest_id']
	elem.meta['newest_id']
	try : 
		NT = elem.meta['next_token'] #token a entrer dans la prochiane requete ? 
	except :
		pdb.set_trace()
		
		
	for ele in elem.data :
		print (ele.text) #-> Premier tweet text 


liste_tweets4=tweepy.Paginator(api.get_users_tweets, user_information.data.id,max_results=100, next_token=NT) #nouvelle requete avec nexttoken issu de la dernière requete
for elem in liste_tweets4 : 
	pdb.set_trace()



	


