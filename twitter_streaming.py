from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import twython


#Variables that contains the user credentials to access Twitter API
access_token = "834114313-cbcheJupdJ6fqhxADgowpnAMHQhjYLD6O6zMLgr8"
access_token_secret = "MDrvRapxjPPubuYdK67qJIWhDjIFSjsAaW31jnWraYkYP"
consumer_key = "RoRUc2cQZWAgUED9mmgRPPiVh"
consumer_secret = "JumucEL6TSpOYU3q3M7hw0PBeEKV2OIHBljGxjtyjpN7YW9bOs"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
id=1163571147323138057
tweet = api.get_status(id)
retweet = api.retweets(id)

# bluthquotes_tweets = api.user_timeline(screen_name = 'bluthquotes', count = 100)
#
# for status in bluthquotes_tweets:
#     print(status)
# replies=[]
# non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#
# for full_tweets in tweepy.Cursor(api.user_timeline,screen_name='bluthquotes',timeout=999999).items(10):
#   for tweet in tweepy.Cursor(api.search,q='to:bluthquotes', since_id=992433028155654144, result_type='recent',timeout=999999).items(1000):
#     if hasattr(tweet, 'in_reply_to_status_id_str'):
#       if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
#         replies.append(tweet.text)
#   print("Tweet :",full_tweets.text.translate(non_bmp_map))
#   for elements in replies:
#        print("Replies :",elements)
#   replies.clear()


print('hi')


#This is a basic listener that just prints received tweets to stdout.
#class StdOutListener(StreamListener):
    #
    # def on_data(self, data):
    #     print (data)
    #     return True
    #
    # def on_error(self, status):
    #     print (status)


#if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    # l = StdOutListener()
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # stream = Stream(auth, l)
    #
    # #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['python', 'javascript', 'ruby'])


