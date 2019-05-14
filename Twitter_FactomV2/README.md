# TweetFCT Version 0.2
Python 3.7 implementation to take tweets from an account via the Twitter API, writes them to the Factom Testnet. This software allows you to create a chain for a specified account and then use the twitter streaming api to write the account's tweets to the chain you created for the account.
All of this is done via docker images. Currently all backend functionality is dockerized and web application is being refined... to be added soon

You can read more about Tweepy, Factom-API, the Twitter API, and Django in the links below:

http://docs.tweepy.org/en/3.7.0/streaming_how_to.html

https://github.com/bhomnick/factom-api

https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters

## Prerequisites

There are several prerequisites you will need to install and changes you will need to make to certain files before you can run the software.
Below are the Instructions to install these dependencies as well as changes you will need to make to run this locally.

### Step 1: Make Sure You have pip installed

If you do not have pip installed, see the documentation on how to properly do so for your machine here: https://pip.pypa.io/en/stable/installing/

### Step 2: Install Docker

This application is run via a container containing a docker image and all of the supporting files. Hence, it will be necessary for you to install docker before you can run the application. To do so, go to https://docs.docker.com/v17.12/install/ and find the appropriate directions for installing docker on your machine. Once you have installed docker and ensured that it is running properly, you should be good to run the application.

### Step 3: Modifying Files

Once you have installed the necessary prerequisites, there are a few changes you will need to make within the files to be able to run on your machine.
Within each folder there is a file titled private.py. Once you have cloned or downloaded this repository, you will need to navigate
to that file within each directory. You should see the following lines:

```
TWITTER_KEY = "Your Twitter Key"
TWITTER_SECRET = "Your Twitter Secret"
TWITTER_APP_KEY = "Your Twitter App Key"
TWITTER_APP_SECRET = "Your Twitter App Secret"

#specify RPC credentials:
FCT_ADDRESS = 'Your FCT Address'
EC_ADDRESS = 'Your EC Address'
```
These are the pertinent API Keys you will need to be able to run the application from your local machine so modify them accordingly.
Secondly, within the the Tweet_WriterV1.py and the Chain_Initiator_V1.py files there is a section where you initialize the factomd and walletd
clients that looks like this:

```
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
```

You will need to replace the IP address in these filese with the IP address of a server you have running on the Factom Testnet.
Lastly, these files up to this point have been used to track tweets for our test account on twitter known as @factombot. If you would 
like to track a different account, you will need to go to the dockerfile in each folder and change the CMD line. Within each of 
these files you will see the following lines:

```
CMD [ "python", "Chain_Initiator_V1.py", "1088451823642595328" ]
```
or
```
CMD [ "python", "Tweet_WriterV1.py", "1088451823642595328" ]
```

The last input for these commands is the Twitter User ID for @Factombot. If you would like to change this and track a different 
account, you will need to modify the User ID. You can find the User ID for any account at https://tweeterid.com/.

## Running the images

Once you have set everything up as you like, you need to first navigate to the Chain_Creator directory. Once within here run

```
docker build .
```
or
```
docker build -t 'your_image_tag' .
```
with whatever tag you wish to name the container. Assuming everything runs as planned, you should see docker successfully download and 
install all of the requirements.

Then run,

```
docker build "your container name"
```

being sure to insert the name of the container you just created. You should see a message printed to your terminal saying 'entry success'
along with some other text. Inside of this you should see the chain id for the chain you just created for the account you will
be tracking on Factom. Wait ~10 minutes after the block is added and then go to https://testnet.factoid.org/dashboard and search the chain_id.
It should pull up an exporer with the chain you instantiated. NOTE: if you have used the same user_ID as an account already being tracked
you may see multiple entries into the chain. CHain ID is derived from the hashes of the external id's used in the entry, so if you want
to create a new chain, you will have to add another external id, however, this is not advised at scale, but is fine for testing purposes. 
Ideally we will want multiple parties to validate a tweet to determine it is legitimate, and will be an added feature in near future development.

Next to stream tweets to this chain, navigate to the Streamer directory in your terminal. From here run:

```
docker build .
```
or
```
docker build -t 'your_image_tag' .
```

Once the container is built run,

```
docker build "your container name"
```
inserting the name of the container you just built. This will initiate the streamer software that will record tweets coming only 
from the account you have specified via the USER ID. The software filters out retweets, replies, mentions, etc and only tracks tweets 
from the account. Every time the account tweets you will see a notification via the terminal and can check the chain of 
tweets periodically for updates of those recorded on the TFA's website.
