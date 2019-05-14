import tweepy #Python twitter API handler
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import settings, random
import identitykeys
from datetime import datetime

#Identity Keys created for Person Committing, Randomly generated now, will need to be automated
private_key, public_key = identitykeys.generate_key_pair()
private = private_key.to_string()
public = public_key.to_string()



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

#name_1 = str(random.random())
#name_2 = str(random.random())
#name_3 = str(random.random())
#chain_content = str(random.random())
#new_chain = walletd.new_chain(factomd, [name_1, name_2, name_3], chain_content, ec_address=ec_address)
#chain_id = new_chain['chainid']

USER_ID = 25073877
chain_id = 'da2ffed0ae7b33acc718089edc0f1d001289857cc27a49b6bc4dd22fac971495' #this will need to be automated to create a new chain for each twitter account tracked

#Define Listening Class
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):  #Tweets will need to be filtered, twitter default pulls ALL tweets with the username you're tracking
        userid = status.user.id
        tweetid = status.id
        date_created = status.created_at
        #print(status)

        if 'realDonaldTrump' in status.text: # returns if the content of the tweet says factombot 
            return
        if status.in_reply_to_user_id_str is userid:  # this filters replies to this twitter ID (avoid retweets & replies)
            return
        
        name = status.user.screen_name #pulls username of tweeter

        """
        ## chain id corresponding to a specific userid
        try:
            chain_content = str(random.random())
            new_chain = walletd.new_chain(factomd, [ str(userid) ], chain_content, ec_address=ec_address)
            chain_id = new_chain['chainid']
        except factom.exceptions.InvalidParams as e:
            print('reveal chain')
            print(factomd.reveal_chain())
        """

        tweet = ''.join(('@', name, ' tweeted: ', status.text)) #combines the the message into a string that can be written to Factom
        fct_entry = {'post': tweet,
                     'Date_Recorded': str(datetime.now()),
                     'tweet': status._json}
        print(name, 'tweeted', status.text)

        try:
            resp = walletd.new_entry(factomd, chain_id, [ name, str(userid), str(tweetid), public], str(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
            print('successfully entered to blockchain')
            print(resp)
        except exceptions.FactomAPIError as e:
            print(e.data)

if __name__ == '__main__':
    StreamListener = StreamListener()
    auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
    api = tweepy.API(auth)

    try:
        stream = tweepy.Stream(auth = api.auth, listener=StreamListener)

        print('hello')
        # print(hashlib.sha256(1088451823642595328))
        stream.filter(follow=[str(USER_ID)]) #change number to whatever twitter ID (or IDs) you want to follow (not the @ handle), you can look up username ID's here: https://tweeterid.com/
        #stream.filter(track=settings.TRACK_TERMS)  #can also track via settings.py
    except KeyboardInterrupt:
        print('Program Exited Gracefully')
        exit(1)
