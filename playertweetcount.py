from pymongo import Connection
import re
from datetime import datetime
from datetime import timedelta

#making connection with mongodb database which is localhost here and port number is 27017
connection = Connection('localhost', 27017)
#database name is dma
db = connection.dma


#method to get all active players and their tweet count is being updated into database returning list of players
def get_player():
	athlete = []
	players = db.active_athletes.find()
	for player in players:
		#print(player)
		athlete.append(player['Player'])
		#print(player['Player'])
		tweet_count = db.tweets.find({'text':{'$regex':player['Player'],"$options":"-i"}}).count()
		db.tweet_count.update({'player':player['Player']},{'$set':{'tweet_count':tweet_count}},True)
		#print(tweet_count)
	return athlete
#end

#method to get count of tweets based on time duration which saves player which returns dictionar of player and count
def get_relative_count(minutes_ago):
	player_tweet_count = {}
	change = 0
	tweet_count_info = db.tweet_count.find()
	for tweet in tweet_count_info:
		player = tweet['player']
		old_count = tweet['tweet_count']
		current_datetime = datetime.now()
		date_time = current_datetime - timedelta(minutes = minutes_ago	)
		#print(now)
		#print(minute_ago)
		new_tweet_count = db.tweets.find({'text':{'$regex':player,"$options":"-i"},'tweet_datetime':{'$gt':date_time}}).count()
		change = new_tweet_count
		#db.tweet_count.update({'player':player},{'$set':{'player':player,'tweet_count':tweet_count,'change':change}},True)
		#print(player)
		#print(change)
		player_tweet_count[player] = change
	return player_tweet_count
#end
		
		
		   	
	


try:
	#get_player()
	get_relative_count(10)
except Exception, e:
	print >> sys.stderr, 'Encountered Exception:', e


