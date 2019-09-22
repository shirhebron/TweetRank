########################## This code only works on tweets from the past 7 days ############################

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pip
import sys
import tweepy
import csv
import time
import json
import logging
import twython
import twitter


tryit={}
all_tweet={}

#Variables that contains the user credentials to access Twitter API
access_token = "834114313-cbcheJupdJ6fqhxADgowpnAMHQhjYLD6O6zMLgr8"
access_token_secret = "MDrvRapxjPPubuYdK67qJIWhDjIFSjsAaW31jnWraYkYP"
consumer_key = "RoRUc2cQZWAgUED9mmgRPPiVh"
consumer_secret = "JumucEL6TSpOYU3q3M7hw0PBeEKV2OIHBljGxjtyjpN7YW9bOs"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,  wait_on_rate_limit=True)


tweet_id=1170370774781374464
print(tweet_id)

tweett = api.get_status(tweet_id)
name = tweett.author._json['screen_name']
cher_tweets = api.user_timeline(screen_name = name, count = 100)

#for status in cher_tweets:
#    print(status)

replies=[]
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
i=0

for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=name,timeout=999999).items(100):
  for tweet in tweepy.Cursor(api.search,q='to:'+name, since_id=tweet_id, result_type='recent',timeout=999999, tweet_mode='extended').items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
      if (tweet.in_reply_to_status_id_str==str(tweet_id)):
        replies.append(tweet)

for elements in replies:
    print("Replies :",'@'+elements.author._json['screen_name'],elements.full_text,elements.retweet_count,elements.favorite_count)
    fields = ['@'+elements.author._json['screen_name'], elements.full_text, elements.retweet_count,elements.favorite_count]
    with open('input_file.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
replies.clear()


