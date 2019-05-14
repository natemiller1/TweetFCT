from django.shortcuts import render
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import tweepy
from TweetApp import private, settings

#Specify Twitter Credentials
auth = tweepy.OAuthHandler(private.TWITTER_KEY, private.TWITTER_SECRET) #Gathers Twitter Keys
auth.set_access_token(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET) #Gathers Twitter APP Keys
api = tweepy.API(auth)

#specify RPC credentials:
fct_address = private.FCT_ADDRESS
ec_address = private.EC_ADDRESS

factomd = Factomd(
    host='http://18.222.184.135:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)

walletd = FactomWalletd(
    host='http://18.222.184.135:8089',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)

USER_ID = 1128123860686200832
chain_id = '406e4a538e8e1d4ea9d699ece3f62c28ef4ac68243ddfae189fe94a91657d2c6' #this will need to be automated to create a new chain for each twitter account tracked
Hash_dict = {'1128306543882059776': '3b74803c43315658f476091b97de647b62d65a67f86e685b603071edbb7cf9d8', 
             '1128306413338529793': 'aab5440dde72163305baeefd731cd30832243e2b16398d4a78335cc4cdf53a1b', 
             '1128306216961179648': 'c746c74b27d8eaf4157adf66c082c2d87b16bcd6a84eeac67849b37cf9945364', 
             '1128306089995460608': '75c786cc4a1241f59fb13c9bf07c90b0ad3a328d62e635f6f5e89b65ea3ab04e', 
             '1128305456194228229': 'fe7fda170bad88b2c726394ba5f7a201048e2143fcafd5c2dfd48eee27a2f013'}

# Create your views here.

class Tweets():

    def __init__(self, chainid, tweetid):
        self.UserandChainID = chainid
        self.tweetid = tweetid

def post_list(request):

    # store ID information
    matchingInformation = []

    # read info from blockchain
    # using 'read_chain()'
    # Create the object 
    # store that in a variable, passed as the third argument in 'render'
    chaininfo = factomd.read_chain(chain_id)
    chaininfo.pop()

    for element in chaininfo:
        print(element)
        CHAINID = element['chainid']
        tweetID = element['extids']
        scribe = tweetID[3]
        tweet_id = tweetID[2]
        entry_hash = Hash_dict[tweet_id]
        status = api.get_status(int(tweet_id))
        tweets = { 'userid' : CHAINID, 'tweetid' : status, 'scribe' : scribe, 'entryhash': entry_hash }

        matchingInformation.append(tweets)

    return render(request, 'TweetApp/post_list.html', { 'tweets' : matchingInformation })
