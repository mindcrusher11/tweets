import json
import wikipedia
import sys
import time
from pymongo import Connection

#making connection with mongodb database which is localhost here and port number is 27017
connection = Connection('localhost', 27017)
#database is dma
db = connection.dma


#save summary of player into mongodb
def save_summary(player,is_ambiguous):
	print(player)
	summary = wikipedia.summary(player).encode('utf8')
	db.player_wiki.update({'wiki_name':player},{'$set':{'summary':summary,'is_ambiguous':is_ambiguous}},True)
	#end

#save wiki page of player into mongoodb 
def save_page(player):
	mongo_obj = {}
	obj_page = wikipedia.page(player)
	mongo_obj['player'] = player
	mongo_obj['title'] = obj_page.title.encode('utf8')
	mongo_obj['url'] = obj_page.url.encode('utf8')
	mongo_obj['content'] = obj_page.content.encode('utf8')
	if(len(obj_page.images) > 0):
		mongo_obj['image'] = obj_page.images[0]
	if(len(obj_page.links) > 0):
		mongo_obj['link'] = obj_page.links[0]
	db.player_wiki_page.update({'player':player},{'$set':mongo_obj},True)
	#end

#retrieve wiki page from wikipedia 
def get_wiki_page(player):
	try:
		print(player)
		save_page(player)
	except wikipedia.exceptions.DisambiguationError as e:	
		print >> sys.stderr, 'inside disambiguation exception'
		print e.options
	except wikipedia.exceptions.HTTPTimeoutError as e:
		time.sleep(10)
		save_page(player)
		print >> sys.stderr, 'Encountered Exception timeout:', e
	except Exception, e:
		print >> sys.stderr, 'Encountered Exception:', e
	#end

#retrieve wiki summary from wikipedia
def get_wiki_summary(player):
	try:
		save_summary(player,False)
	except wikipedia.exceptions.DisambiguationError as e:	
		db.player_wiki.update({'wiki_name':player},{'$set':{'is_ambiguous':True,'options':e.options,'wiki_name':player + ' (basketball)'}},True)
		print >> sys.stderr, 'inside disambiguation exception'
		print e.options
	except wikipedia.exceptions.HTTPTimeoutError as e:
		time.sleep(10)
		save_summary(player,False)
		print >> sys.stderr, 'Encountered Exception timeout:', e
	except Exception, e:
		db.player_wiki.update({'wiki_name':player},{'$set':{'is_ambiguous':True}},True)
		print >> sys.stderr, 'Encountered Exception:', e
	#end
	
		
#get summary of all players from wikipedia		
def get_summary():
	json_data = db.player_wiki.find()
	for player in json_data:
		get_wiki_summary(player['wiki_name'].encode('utf8'))
	#end

#get summary of all players from wikipedia which are ambiguous and summary is retrieved again with updated wikiname
def get_summary_ambiguous():
	json_data = db.player_wiki.find({'is_ambiguous':True})
	for player in json_data:
		get_wiki_summary(player['wiki_name'])
	#end

#get page of all players 
def get_page():
	json_data = db.player_wiki.find(timeout=False)
	for player in json_data:
		get_wiki_page(player['wiki_name'].encode('utf8'))
	#end

#get page of all players which are ambiguous and need to retrieved from wikipedia	
def get_page_ambiguous():
	json_data = db.player_wiki.find({'is_ambiguous':True},timeout=False)
	for player in json_data:
		get_wiki_page(player['wiki_name'].encode('utf8'))
	#end


#read json file and save into mongodb
def save_players_from_json(file_path):
	with open(file_path) as json_file:
		json_data = json.load(json_file)
		for player in json_data:
			#db.player_wiki.insert({'player':player['player_name'],'wiki_name':player['player_name']})
			db.player_wiki_all.insert(player)
	#end



#get_page()
get_summary()
#save_players_from_json("/home/hduser/matchup-source/data/league/nba/spotrac_contracts.json")	
#try:
#get_summary_ambiguous("/home/hduser/matchup-source/data/league/nba/spotrac_contracts.json")
#except:
#	print('exception caught in get summary method')
	
