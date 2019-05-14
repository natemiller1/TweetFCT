import tweepy #Python twitter API handler
from factom import Factomd, FactomWalletd, exceptions #python Factom API
import settings, random
import identitykeys
from datetime import datetime
import sys

#Identity Keys created for Person Committing, Randomly generated now, will need to be automated
private_key, public_key = identitykeys.generate_key_pair()
private = private_key.to_string()
public = public_key.to_string()
message = b'TwitterBank Record'
signature = private_key.sign(message)


# Specify RPC credentials so you can utilize Factom:
fct_address = settings.FCT_ADDRESS
ec_address = settings.EC_ADDRESS

factomd = Factomd(
    host='http://your_ip_address:8088',
    fct_address=fct_address,
    ec_address=ec_address,
    username='rpc_username',
    password='rpc_password'
)

walletd = FactomWalletd(
    host='http://your_ip_address:8089',
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

chain_id = 'f8ac360c2b98d193a7da40ff9ee649275e2789141ca7a0a816e1086e9fe0b79a' #this will need to be automated to create a new chain for each twitter account tracked

#Define Listening Class
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):  #Tweets will need to be filtered, twitter default pulls ALL tweets with the username you're tracking
        
        print('Gathering Tweet...')
        
        if from_creator(status):
            
            print('Tweet Filtered!')
            
            try:
                userid = status.user.id
                tweetid = status.id
                name = status.user.screen_name #pulls username of tweeter
                print('@',name, 'tweeted', status.text) #prints tweet to terminal
                
                fct_entry = {'Date_Recorded': str(datetime.now()),
                     'tweet': status._json}
                print('Sending Tweet to Factom!')
                
                try:
                    resp = walletd.new_entry(factomd, chain_id, 
                                             [ 'TwitterBank Record',str(userid), str(tweetid),public, signature],
                                             str(fct_entry), ec_address=ec_address) # makes entry into the factom testnet
                    
                    print(' Tweet Successfully Entered Into the Factom Testnet!')
                    print(resp)
                    
                except exceptions.FactomAPIError as e:
                    print(e.data)
                
                print('Tweet Processed! Waiting For More Tweets to Factomize...')
                return True
            
            except BaseException as e:
                print("Error on_data %s" % str(e))
                return True
            
       
##### The Main function. The series of functions executed when you run the program from the command line
if __name__ == '__main__':
    
    print('Streamer On, Ready to Factomize Some Tweets!')
    StreamListener = StreamListener() #Turns Stream Listener Class On
    
    auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET) #Gathers Twitter Keys
    auth.set_access_token(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET) #Gathers Twitter APP Keys
    api = tweepy.API(auth)
    USER_ID = sys.argv[1:] #the User Id for the twitter account you would like to follow, passed as argument from command line when you run the program
    user = USER_ID[0] #Takes the User ID you passed and isolates the variable so no longer a list variable
    print('User ID Gathered:' + str(user))
    try:
        stream = tweepy.Stream(auth = api.auth, listener=StreamListener)
        stream.filter(follow=[str(user)]) #change number to whatever twitter ID (or IDs) you want to follow (not the @ handle), you can look up username ID's here: https://tweeterid.com/
        
    except KeyboardInterrupt:
        print('Program Exited Gracefully')
        exit(1)
