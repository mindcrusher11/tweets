# Tweets Requirements and Installation

<<<<<<< HEAD
Prerequisites:

Python should be installed 2.7

MongoDb should be installed 

Tweepy Library should be installed in python

Pymongo should be installed in python for mongodb access using python

wikipedia package should be installed in python

How to Install:

MongoDB installation :

Mongodb can be downloaded from mongodb.org website

Version 3.0 is more preferable 

Mongodb is scalable,json support document nosql database

mongod executable is server 

mongo executable is client 

Tweepy Installation :

tweepy can be installed using pip or easy setup

sudo pip install tweepy

Pymongo Installation :

pymongo can also be installed using pip

sudo pip install pymongo

Wikipedia Installation :

wikipedia can also be installed using pip

sudo pip install wikipedia

Above code files can be executed by using command 

python filename



=======
##Prerequisites:

1. Python 2.7
1. MongoDb
1. `tweepy`, `pymongo`, `wikipedia` python libraries

##How to Install:

###MongoDB:

Mongodb can be downloaded from mongodb.org website.  Version 3.0 is more preferable.  Mongodb is scalable, json support document nosql database.  `mongod` executable is the server.  `mongo` executable is the client. 

Mongodb can be installed from terminal using command

sudo apt-get install mongodb

Or 

Using Binaries  

MongoDB binaries can be downloaded from 'https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1204-3.0.1.tgz' for ubuntu 12.04 ,other versions can be downloaded from 'https://www.mongodb.org/downloads'

Extract binaries from above file using:
tar xzf  mongodb-linux-x86_64-ubuntu1204-3.0.1.tgz

##Prerequisites for Mongodb:

Create directory for mongodb storage it should be /data/db

sudo mkdir /data/db

change access of above directory to read write mode

Port Number '27107' should be free

##Execute MongoDB

Now Move to mongodb binaries folder 

cd mongodb*

execute mongodb server using
'./mongod'

execute mongodb client using
'./mongo'

Now we can access mongodb shell as it is up and running now


###Python modules

    sudo pip install tweepy
    sudo pip install pymongo
    sudo pip install wikipedia

##How to run:

#Prerequisites for twitter_to_mongo

##Active Player List should be in mongodb

Json Data can be imported to mongodb using :

'mongoimport --db dma --collection active_athletes --file filename.json'


#twitter-to-mongo.py 

File to fetch tweets from twitter streaming api using player names as filter parameters 
Streaming api has constraint of maximum 400 filter parameters so twitter-to-mongo.py retrieve tweets of first '400' players with my credentials

#twitter-to-mongo_re.py 

To overcome 400 limit constraint different credentials are used for this api and rest of players are passed to this streaming api as filter parameter 

Above files retrieve tweets from streaming api with different credentials and different players list as arguments to track parameter of streaming api.

Active Players List is retrieved from mongodb database named dma and collection(Table) active_athletes 

Tweets are stored into mongodb

#weekiplayer.py

code to download wikipedia data for player

summary data from wikipedia
page data from wikipedia downloaded and saved into mongodb

#playertweetcount.py
code to count number of tweets for each player using time interval as 'minutes' 
argument should be minutes so that number of tweets for each player in that mnutes duration can be eavluated from mongodb tweets database.

 
>>>>>>> 9a6731d6f0373e24be9dd6648f21f594b48ac78d

