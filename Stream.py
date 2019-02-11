import tweepy #Python twitter API handler
from factom import Factomd, FactomWalletd #python Factom API
import settings

#specify RPC credentials:
fct_address = settings.FCT_ADDRESS
ec_address = settings.EC_ADDRESS

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

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

#Define Listening Class
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):  #Tweets will need to be filtered, twitter default pulls ALL tweets with the username you're tracking
        if 'factombot' in status.text:
            return
        if status.in_reply_to_user_id_str is 1088451823642595328:  #this filters replies to this twitter ID
            return
        
        name = status.user.screen_name #pulls username of tweeter
        
        fct_entry = ''.join(('@', name, ' tweeted: ', status.text)) #combines the the message into a string that can be written to Factom
        print(name, 'tweeted', status.text)
        
        walletd.new_entry(factomd, chain_id, ['random', 'entry', 'id'], fct_entry, ec_address=ec_address) #makes entry into the factom testnet

StreamListener = MyStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=StreamListener)

stream.filter(follow=["1088451823642595328"]) #change number to whatever twitter ID (or IDs) you want to follow (not the @ handle), you can look up username ID's here: https://tweeterid.com/
#stream.filter(track=settings.TRACK_TERMS)  #can also track via settings.py
