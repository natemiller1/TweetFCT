import tweepy #Python twitter API handler
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import settings, random
import identitykeys
from datetime import datetime
import sys

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

# This is a function to filter all tweets for the user_id being streamed besides their own tweets
def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        print('removed retweets')
        return False
    
    elif status.in_reply_to_status_id != None:
        print('removed replies')
        return False
        
    elif status.in_reply_to_screen_name != None:
        print('removed replies')
        return False
    
    elif status.in_reply_to_user_id != None:
        print('removed replies')
        return False
    else:
        return True
'''
Below is the Twitter ID for @factombot and the chain_ID on the Facom testnet we have been writing to for testing.
Automating these will be critical to future work and establishing a robust software package. If you wish to track a different
account on the same chain you can change the user id here to twitter id you wish to follow, but you will also have to generate
a new chain first before you can change the chain id.
'''
chain_id = 'da2ffed0ae7b33acc718089edc0f1d001289857cc27a49b6bc4dd22fac971495' #this is the chain ID we have been writing to for test purposes

#Define Listening Class
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):  #Turns on the listener class. Filters only for tweets directly from @factombot (no retweets)
        print('Gathering Tweet...')
        if from_creator(status): #Filters tweets with handle of user_id that is being tracked so only his or her tweets from her accounts are tracked
            print('Tweet Filtered!')
            try:
                userid = status.user.id #pulls user id from json output of the tweet status
                tweetid = status.id #pulls the tweet id from the json output of the tweet status
                name = status.user.screen_name #pulls username of tweeter
                print('@',name, 'tweeted', status.text) #prints tweet to terminal
                
                """
                Below we define what the content is that will be entered into the entry on the Factom Blockchain. We make a condensed entry
                that just says "@factombot tweeted: _____" in case a user is not interested in the JSON output. We also put the time at which
                the tweet was recorded and the entire JSON output for the status posted by @factombot. All of this information is saved to a 
                dictionary and entered as a single entry into the content portion of the blockchain entry for the tweet.
                """
                
                fct_entry = {'Date_Recorded': str(datetime.now()),
                     'tweet': status._json}
                print('Sending Tweet to Factom!')
                
                '''
                Below is where we actually write the tweet to the Factom blockchain. Using the walletd call from the factom api, we submit a 
                new entry to the chain we defined earlier. We must pass it the following paramaters in order to to successfully submit the entry.
                1. factomd --> we activated this earlier
                2. chain_id --> the chain_id we defined earlier for the @factombot account
                3. external_IDs --> these are the external id's for the entry that will be written to the blockchain for the above content.
                    we chose the following(all must be string type):
                    a.) TwitterBank Record --> tentative name for record being submitted to Factom
                    b.) name --> twitter handle (@factombot)
                    c.) userid --> the twitter id for the handle (the user/twitter id corresponding to @factombot here)
                    d.) tweetid --> the ID number for the actual tweet itself
                    e.) public --> the string of the randomly generated public key used to sign (will correspond to identifier for person
                        submitting tweet to the Factom blockchain at a later time)
                4. fct_entry --> the string for the content variable we defined above
                4.) ec_address --> the ec_address we defined and activated earlier
                '''
                
                try:
                    #Below is what is entered into the content portion of the entry to the blockchain
                    resp = walletd.new_entry(factomd, chain_id, 
                                             [ 'TwitterBank Record','TwitterHandle: ' + name, 'userid: ' + str(userid), 'tweetid: ' + str(tweetid),'SignedBy: ' + public],
                                             str(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
                    
                    print(' Tweet Successfully Entered Into the Factom Testnet!') #prints to your command line so you know that it you were successful
                    print(resp)  #prints the entry information to commandline. Once next block is added to blockchain you can view on https://testnet.factoid.org/dashboard
                    
                except exceptions.FactomAPIError as e:
                    print(e.data)#error handling for factom-api when entry fails
                
                print('Tweet Processed! Waiting For More Tweets to Factomize...')
                return True
            
            except BaseException as e:
                print("Error on_data %s" % str(e))
                return True
'''
Below is the sequence of functions that is initiated once you run python master.py from the command line.
'''
if __name__ == '__main__':
    StreamListener = StreamListener() #initializes stream listener
    auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET) #authorizes your twitter key credentials
    auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET) #authorizes your twitter app credentials
    api = tweepy.API(auth) #authorizes your access to the twitter api to stream
    USER_ID = sys.argv[1:] #the User Id for the twitter account you would like to follow, passed as argument from command line when you run the program
    user = USER_ID[0] #Takes the User ID you passed and isolates the variable so no longer a list variable

    try:
        stream = tweepy.Stream(auth = api.auth, listener=StreamListener) #sets the stream

        print('Streamer On, Ready to Factomize Some Tweets!') #prints to command line to let you know streamer is engaged

        stream.filter(follow=[str(user)]) #change number to whatever twitter ID (or IDs) you want to follow (not the @ handle), you can look up username ID's here: https://tweeterid.com/
        
    except KeyboardInterrupt:
        print('Program Exited Gracefully')
        exit(1)
