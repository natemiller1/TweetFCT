# TweetFCT Version 0.1
Python 3.7 implementation to take tweets from Twitter API, write them to the Factom Testnet, and use a Django based web-app to display them on webpage attatched to your localhost. Second Iteration on Proof of Concept!

You can read more about Tweepy, Factom-API, the Twitter API, and Django in the links below:

http://docs.tweepy.org/en/3.7.0/streaming_how_to.html

https://github.com/bhomnick/factom-api

https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters

https://www.djangoproject.com/


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

***Step 4: Install Docker***

This application is run via a container containing a docker image and all of the supporting files. Hence, it will be necessary for you to install docker before you can run the application. To do so, go to https://docs.docker.com/v17.12/install/ and find the appropriate directions for installing docker on your machine. Once you have installed docker and ensured that it is running properly, you should be good to run the application.

**Starting up** 

Once you have completed the installation of all of the prereqs, navigate to the folder in this repo titled TweetFCT_V0.1. Clone that repo and you should have everything needed to run the application. If you are new to how docker containers work, read the file titled 'Docker_setup.txt' for a step by step guide on how to setup and deploy a containerized docker image as well as some of the changes you may need to make to the files when running on your local machine. There is a separate README.md file within that folder that explains how each of the pertinent files operate for further information.


