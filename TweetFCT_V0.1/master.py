import tweepy #Python twitter API handler
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import settings, random
import identitykeys
from datetime import datetime

#Identity Keys created for Person Committing, Randomly generated now, will need to be automated
private_key, public_key = identitykeys.generate_key_pair() #randomly generates a key pair for an identity for person running software
private = private_key.to_string() #string of randomly generated private key
public = public_key.to_string() #string of randomly generated public key, will be used later



#specify RPC credentials:
fct_address = settings.FCT_ADDRESS
ec_address = settings.EC_ADDRESS

factomd = Factomd(
    host='http://YOUR_IP_ADDRESS:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)

walletd = FactomWalletd(
    host='http://YOUR_IP_ADDRESS:8089'',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)
'''
Below is the Twitter ID for @factombot and the chain_ID on the Facom testnet we have been writing to for testing.
Automating these will be critical to future work and establishing a robust software package. If you wish to track a different
account on the same chain you can change the user id here to twitter id you wish to follow, but you will also have to generate
a new chain first before you can change the chain id.
'''
USER_ID = 1088451823642595328 #This is the @factombot twitter ID
chain_id = 'da2ffed0ae7b33acc718089edc0f1d001289857cc27a49b6bc4dd22fac971495' #this is the chain ID we have been writing to for test purposes

#Define Listening Class
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):  #Turns on the listener class. Filters only for tweets directly from @factombot (no retweets)
        userid = status.user.id #pulls user id from json output of the tweet status
        tweetid = status.id #pulls the tweet id from the json output of the tweet status
        date_created = status.created_at #pulls the time at which the tweet was made from the json ouput of the tweet status
        print(status) #This prints the status that was posted by @factombot. Not necessary and can be turned off/deleted left for testing purposes

        if 'factombot' in status.text: # returns if the content of the tweet says factombot 
            return
        if status.in_reply_to_user_id_str is userid:  # this filters replies to this twitter ID (avoid retweets & replies)
            return
        
        name = status.user.screen_name #pulls username of tweeter, in this case factombot
        
        """
        Below we define what the content is that will be entered into the entry on the Factom Blockchain. We make a condensed entry
        that just says "@factombot tweeted: _____" in case a user is not interested in the JSON output. We also put the time at which
        the tweet was recorded and the entire JSON output for the status posted by @factombot. All of this information is saved to a 
        dictionary and entered as a single entry into the content portion of the blockchain entry for the tweet.
        """
        tweet = ''.join(('@', name, ' tweeted: ', status.text)) #combines the the message into a string that can be written to Factom
        
        #Below is what is entered into the content portion of the entry to the blockchain
        fct_entry = {'post': tweet,
                     'Date_Recorded': str(datetime.now()),
                     'tweet': status._json}
        
        #Below will print the tweet to your command line. Not necessary, but useful as it lets you know the streamer is working
        print(name, 'tweeted', status.text)
        
        '''
        Below is where we actually write the tweet to the Factom blockchain. Using the walletd call from the factom api, we submit a 
        new entry to the chain we defined earlier. We must pass it the following paramaters in order to to successfully submit the entry.
        1. factomd --> we activated this earlier
        2. chain_id --> the chain_id we defined earlier for the @factombot account
        3. external_IDs --> these are the external id's for the entry that will be written to the blockchain for the above content.
            we chose the following(all must be string type): 
            a.) name --> twitter handle (@factombot)
            b.) userid --> the twitter id for the handle (the user/twitter id corresponding to @factombot here)
            c.) tweetid --> the ID number for the actual tweet itself
            d.) public --> the string of the randomly generated public key used to sign (will correspond to identifier for person
            submitting tweet to the Factom blockchain at a later time)
        4. fct_entry --> the string for the content variable we defined above
        4.) ec_address --> the ec_address we defined and activated earlier
        '''
        try:
            resp = walletd.new_entry(factomd, chain_id, [ "TwitterBank Record", str(userid), str(tweetid), public], str(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
            print('successfully entered to blockchain') #prints to your command line so you know that it you were successful
            print(resp) #prints the entry information to commandline. Once next block is added to blockchain you can view on https://testnet.factoid.org/dashboard
        except exceptions.FactomAPIError as e:
            print(e.data) #error handling for factom-api when entry fails
'''
Below is the sequence of functions that is initiated once you run python master.py from the command line.
'''
if __name__ == '__main__':
    StreamListener = StreamListener() #initializes stream listener
    auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET) #authorizes your twitter key credentials
    auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET) #authorizes your twitter app credentials
    api = tweepy.API(auth) #authorizes your access to the twitter api to stream

    try:
        stream = tweepy.Stream(auth = api.auth, listener=StreamListener) #sets the stream

        print('hello') #prints hello to command line to let you know streamer is engaged

        stream.filter(follow=[str(USER_ID)]) #change number to whatever twitter ID (or IDs) you want to follow (not the @ handle), you can look up username ID's here: https://tweeterid.com/
        #stream.filter(track=settings.TRACK_TERMS)  #can also track via settings.py
        
    except KeyboardInterrupt:
        print('Program Exited Gracefully')
        exit(1)
