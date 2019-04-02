from django.shortcuts import render
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import settings, random

#specify RPC credentials:
fct_address = settings.FCT_ADDRESS
ec_address = settings.EC_ADDRESS

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

USER_ID = 1088451823642595328
chain_id = 'da2ffed0ae7b33acc718089edc0f1d001289857cc27a49b6bc4dd22fac971495' #this will need to be automated to create a new chain for each twitter account tracked

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

    for element in chaininfo:
        USERandCHAINID = element['chainid']
        tweetID = element['extids']
        tweets = { 'userid' : USERandCHAINID, 'tweetid' : tweetID[0] }

        matchingInformation.append(tweets)

    return render(request, 'readtweets/post_list.html', { 'tweets' : matchingInformation })