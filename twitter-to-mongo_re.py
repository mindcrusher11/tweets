# ===============================================
# twitter-to-mongo.py v1.0 Created by gaurhari
# ===============================================
from pymongo import Connection
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
import sys

# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
connection = Connection('localhost', 27017)
db = connection.dma
db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweets


# Add the keywords you want to track. They can be cashtags, hashtags, or words.
keywords = ['$goog', '#funny', 'ipad']

# Optional - Only grab tweets of specific language
language = ['en']

#Variables that contains the user credentials to access Twitter API 
access_token = "374363728-BCe1rusHWiVPBHDCQ5RoketbfaNePuHXTeJja7W6"
access_token_secret = "cMyNaQwVzxtXKqSG0jjlI1H6avEoMbvZ36pB7Zr5dPEN0"
consumer_key = "hhYq78kZ6VkAp4Q4pXzuKCOkA"
consumer_secret = "A468W3FnFd9WcL2PXYeRO0iLWnu90761HkKHijXRXqmgtR1bpk"

#consumer_key="IzxpLmPU7bcH6mkoEPhrDgCRz"
#consumer_secret="vqo6m3JU1TKRhSGwDHg8IxuvOZ4IGiiXdFxn8kgwuRTb5ijogZ"
#access_token="100311379-VJOuaxitBtDCq2WK11HXo3ROQSzDME7Ut1vL3AoI"
#access_token_secret="Ga3VCILMJkBd898Ewd3excvzicDPpepiRKvX0z9YMLM1q"

# The below code will get Tweets from the stream and store only the important fields to your database
class StdOutListener(StreamListener):

	def on_data(self, data):
		try:
			# Load the Tweet into the variable "t"
			t = json.loads(data)
			print(t)
			# Pull important data from the tweet to store in the database.
			tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
			username = t['user']['screen_name']  # The username of the Tweet author
			followers = t['user']['followers_count']  # The number of followers the Tweet author has
			text = t['text']  # The entire body of the Tweet
			hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
			dt = t['created_at']  # The timestamp of when the Tweet was created
			language = t['lang']  # The language of the Tweet
			tweet_datetime = datetime.now() # current date time value
			location = t['user']['location'] #location of user
			coordinates = t['coordinates']
			# Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
			created = datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

			# Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
			tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created,'tweet_datetime':tweet_datetime,'location':location,'coordinates':coordinates}

			# Save the refined Tweet data to MongoDB
			collection.save(tweet)

			# Optional - Print the username and text of each Tweet to your console in realtime as they are pulled from the stream
			print username + ':' + ' ' + text
			return True

		except Exception, e:
			print >> sys.stderr, 'Encountered Exception:', e
			pass
			return True

		def on_delete(self, status_id, user_id):
			print 'Got DELETE message:', status_id, user_id
			return True # Don't kill the stream

		def on_limit(self, track):
			"""Called when a limitation notice arrvies"""
			print 'Got Rate limit Message', str(track)
			return True # Don't kill the stream

		def on_error(self, status_code):
			print 'Encountered error with status code:', status_code
			return True # Don't kill the stream

	# Prints the reason for an error to your console
	#def on_error(self, status):
	#print status
	#return True

	def on_timeout(self):
		print 'Timeout...'
		return True # Don't kill the stream
	def on_stall_warning(self, status):
		print "Got Stall Warning message",str(status)
		return True # Don't kill the stream

# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
	try:
		#list of active players which is stored in mongodb so list need to be there in mongodb
		active_player = db.active_athletes
		players = []
		athlete_list = active_player.find({}).skip(400)
		for athletes in athlete_list:
			players.append(athletes['Player'])
	
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		#list of player names is passed to streaming api to filter tweets based on player names
		stream = Stream(auth, l)
		stream.filter(track=players)
		
	except Exception, e:
		print >> sys.stderr, 'Encountered Exception:', e
	finally:
		stream.disconnect()
