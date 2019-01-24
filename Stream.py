import tweepy #Python twitter API handler
from factom import Factomd, FactomWalletd #python Factom API

#specify RPC credentials:
fct_address = 'FA3xxxxxxx'
ec_address = 'EC34xxxxxx'

factomd = Factomd(
    host='http://xx.xx.xx.xx:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)

walletd = FactomWalletd(
    host='http://xx.xx.xx.xx:8089',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)
chain_id = 'da2ffed0ae7b33acc718089edc0f1d001289857cc27a49b6bc4dd22fac971495' #this will need to be automated to create a new chain for each twitter account tracked

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Define Listening Class
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):  #Tweets will need to be filtered, twitter default pulls ALL tweets with the username you're tracking
        if '@realDonaldTrump'in status.text:
            return
  #      if '@RealDonaldTrump' in status.text:
   #         return
        if '@realdonaldtrump' in status.text:
            return
        if 'factombot' in status.text:
            return
        if status.in_reply_to_user_id_str is 25073877:  #this filters replies to this twitter ID
            return
        print(status.text)
        walletd.new_entry(factomd, chain_id, ['random', 'entry', 'id'], status.text, ec_address=ec_address) #makes entry into the factom testnet

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(follow=["2211149702"]) #change number to whatever twitter ID (or IDs) you want to follow (not the @ handle), you can look up username ID's here: https://tweeterid.com/
