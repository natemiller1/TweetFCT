# TweetFCT Version 0.1
Python 3.7 implementation to take tweets from Twitter API, write them to the Factom Testnet, and use a Django based web-app to display them on webpage attatched to your localhost. Second Iteration on Proof of Concept!

You can read more about Tweepy, Factom-API, the Twitter API, and Django in the links below:

http://docs.tweepy.org/en/3.7.0/streaming_how_to.html

https://github.com/bhomnick/factom-api

https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters

https://www.djangoproject.com/

**Pre-Req:** If you are just landing on this page, go back to https://github.com/natemiller1/TweetFCT, and read how to set up your environment to run this program. You also may need to install django if you have not done so already. Directions on how to do so are posted below.

***Step 1: Make Sure You have pip installed***

If you do not have pip installed, see the documentation on how to properly do so for your machine here: https://pip.pypa.io/en/stable/installing/

***Step 2: Activate Your Virtual Environment***

From the command line run the following lines to activate a python virutal environment:

```
python3 -m venv venv
source venv/bin/activate
```

***Step 3: Install Django***

Once pip is installed on your machine and you have activated and are working in your virtual environment, run the following line from the command line to install Django:

```
pip install Django
```

You should be good to operate from here, just clone this github repository. Directions on how to operate the program are posted below.

**Starting up** 

Once installed you can run the program contents form the command line as follows:

**To Stream Tweets to Factom**

From the command line run

```
python master.py
```

If successful, you should see the commandline say 'hello' and a stream listener will be engaged that will notify you from the command line every time the account @factombot tweets and print the contents of the tweet. It will then print 'successful entry to the blockchain' as well as the contents of the entry. After a few minutes, the entry should be displayed on the Factom blockchain (once the next block is added to the blockchain). To check go to https://testnet.factoid.org/dashboard and enter the chain id that is displayed. Once you navigate to that page you can navigate to the entry hash for the most recent tweet or read through past tweets.

**To Deploy the WebApp locally**

from the command line, navigate to the directory where you cloned this github repository. Once there, you must activate the python virtual environment you installed to deploy a django web app. To do so, run the following commands:

```
source myvenv/bin/activate
python manage.py runserver
```

If successful, a url with your local host and the port you're streaming to should be displayed. Copy and paste this url into your browser of choice and the web page should be diplayed of the Tweets written by @factombot to the Factom blockchain. To cease streaming the webppage from your machine go back to your command line and click control + C. This should terminate the stream. Then run the following line from the command line to deactivate your python virtual environment:

```
deactivate
```

Next Steps:
1. Automate everything so the program does not need to rely on hardcoded key handling/twitter account information
2. Figure out a way to incorporate identity of the one posting tweets to Factom, that will be a universal identity for that user.
3. Quickly determine the number of users who have validated a tweet as legitimate or not.
4. Incorporate this with database
