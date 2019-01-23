import tweepy, harmony_connect_client

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Define Listening Class
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(follow=["2211149702"]) #change number to whatever twitter ID you want to follow (not the @ handle)
