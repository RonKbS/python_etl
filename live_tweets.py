import os
import json
from datetime import datetime, timedelta
from collections import deque

# third-party libs
import tweepy
import mysql.connector
from mysql.connector import Error
from dateutil import parser
from flask_socketio import SocketIO, emit

from analyze_tweets import *


cons_k = os.environ.get('consumer_key')
cons_s = os.environ.get('consumer_secret')
acc_t = os.environ.get('access_token')
acc_t_s = os.environ.get('access_token_secret')
password = os.environ.get('DB_PASSWORD')



def connect(
    username, created_at, tweet, retweet_count, place, location
):
	try:
		con = mysql.connector.connect(
            host='localhost',
            database='tweet',
            user='root',
            password=password,
            charset='utf8'
		)

		if con.is_connected():
			cursor = con.cursor()
			query = "INSERT INTO tweets (username, created_at, tweet, retweet_count,place, location) VALUES (%s, %s, %s, %s, %s, %s);"
			cursor.execute(query, (username, created_at, tweet, retweet_count, place, location))
			try:
				con.commit()
			except Error as e:
				print(e)

	except Error as e:
		print(e)

	cursor.close()
	con.close()

	return



def clear_db():
	try:
		con = mysql.connector.connect(
            host='localhost',
            database='tweet',
            user='root',
            password=password,
            charset='utf8'
		)

		if con.is_connected():
			cursor = con.cursor()
			query = "TRUNCATE TABLE tweets"
			cursor.execute(query)
			try:
				con.commit()
			except Error as e:
				print(e)

	except Error as e:
		print(e)

	cursor.close()
	con.close()

	return


# Tweepy class to access Twitter API

class Streamlistener(tweepy.StreamListener):

	def on_connect(self):
		print("You are connected to the Twitter API")

	def on_error(self):
		if status_code != 200:
			print("error found")

			# returning false disconnects the stream
			return False

	def on_data(self,data):
		try:
			raw_data = json.loads(data)

			if 'text' in raw_data:
				username = raw_data['user']['screen_name']
				created_at = parser.parse(raw_data['created_at'])
				tweet = raw_data['text']
				retweet_count = raw_data['retweet_count']

				if raw_data['place'] is not None:
					place = raw_data['place']['country']
					print(place)
				else:
					place = None

				if raw_data['user']['location'] is not None:
					location = raw_data['user']['location']
					print(location)
				else:
					location = None

				# insert data just collected into MySQL database
				connect(username, created_at, tweet, retweet_count, place, location)

				print("Tweet colleted at: {} ".format(str(created_at)))

				global now
				time_limit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				if int(time_limit[17:19]) - int(now[17:19]) == 15:

					print('time_limit_______', time_limit)
					print('now_______', now)

					now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

					t = TweetObject( host='localhost', database='tweet', user='root')
					data  = t.MySQLConnect("SELECT created_at, tweet FROM `tweet`.`tweets`;")
					clear_db()

		except Error as e:
			print(e)




if __name__== '__main__':

	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	auth = tweepy.OAuthHandler(cons_k, cons_s)
	auth.set_access_token(acc_t, acc_t_s)
	api =tweepy.API(auth, wait_on_rate_limit=True)



	# create instance of Streamlistener
	listener = Streamlistener(api = api)
	stream = tweepy.Stream(auth, listener = listener)



	track = ['okay', 'wow', 'the', 'this']
	stream.filter(track = track, languages = ['en'])
