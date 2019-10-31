import mysql.connector
from mysql.connector import Error
import tweepy
import json
from dateutil import parser
import time
import os


cons_k = os.environ.get('CONSUMER_KEY')
cons_s = os.environ.get('CONSUMER_SECRET')
acc_t = os.environ.get('ACCESS_TOKEN')
acc_t_s = os.environ.get('ACCESS_TOKEN_SECRET')
pd = os.environ.get('DB_PASSWORD')

def connect(
    username, created_at, tweet, retweet_count, place , location
):
	try:
		con = mysql.connector.connect(
            host = 'localhost',
            database='tweet',
            user='root',
            password = pd,
            charset = 'utf8'
        )

		if con.is_connected():
			cursor = con.cursor()
			query = "\
                    INSERT INTO tweets\
                    (username, created_at, tweet, retweet_count,place, location)\
                    VALUES (%s, %s, %s, %s, %s, %s);
                "
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

				location = raw_data['user']['location']

				#insert data just collected into MySQL database
				connect(username, created_at, tweet, retweet_count, place, location)
				print("Tweet colleted at: {} ".format(str(created_at)))

		except Error as e:
			print(e)


