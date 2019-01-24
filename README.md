# TweetFCT
Python 3.7 implementation to take tweets from Twitter API and write to the Factom Testnet. Very basic proof of concept!

You can read more about Tweepy, Factom-API, and the Twitter API in the below links:

http://docs.tweepy.org/en/3.7.0/streaming_how_to.html

https://github.com/bhomnick/factom-api

https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters

**Starting up** (this isn't required, feel free to use whatever your favorite coding method is):

Make sure you have git and python 3 installed (type git and python to double check)

The code below will launch a virtual environment and jupyter notebook in your browser 


**Linux**

```
git clone https://github.com/natemiller1/TweetFCT.git
cd TweetFCT
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
jupyter notebook
```

**PC**

From powershell:
```
git clone https://github.com/natemiller1/TweetFCT.git
cd TweetFCT
python -m virtualenv venv
venv/Scripts/activate
python -m pip install -r requirements.txt
jupyter notebook
```

The stream.py file contains necessary code for a quick POC to stream tweets and write them to the Factom Testnet. Here are some thoughts on additional things needed:

Other ideas:
1. The on_status is important, we need to filter out random replies/tweets that aren't from the person we're tracking BUT we don't want to accidentally filter out real tweets (or allow the person to avoid being tracked by meeting one of our filtering criteria)
2. want to track their retweets as well
3. Plenty of other cool niceties to add as well - we could automatically tweet when certain factom entries are made, we could also run a website that streams the tweets and updates when they're factomized.
4. We'll need a database of twitter accounts to follow
5. Right now, it just records the text of the tweet not who made it, so I'll fix that soon.
6. Will want a separate chain for each person we track? Could do either, will want to automate chain creation and decide a good structure for the entry ID
7. Will possibly need a database to record tweets as they come in - may provide additional functionality down the road. Right now code streams tweets directly to Factom.
