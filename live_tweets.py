import mysql.connector
from mysql.connector import Error
import tweepy
import json
from dateutil import parser
import os


cons_k = os.environ.get('consumer_key')
cons_s = os.environ.get('consumer_secret')
acc_t = os.environ.get('access_token')
acc_t_s = os.environ.get('access_token_secret')
pd = os.environ.get('DB_PASSWORD')


def connect(
    username, created_at, tweet, retweet_count, place, location
):
	try:
		con = mysql.connector.connect(
            host='localhost',
            database='tweet',
            user='root',
            password=pd,
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

				# insert data just collected into MySQL database
				connect(username, created_at, tweet, retweet_count, place, location)
				print("Tweet colleted at: {} ".format(str(created_at)))

		except Error as e:
			print(e)




if __name__== '__main__':

	auth = tweepy.OAuthHandler(cons_k, cons_s)
	auth.set_access_token(acc_t, acc_t_s)
	api =tweepy.API(auth, wait_on_rate_limit=True)



	# create instance of Streamlistener
	listener = Streamlistener(api = api)
	stream = tweepy.Stream(auth, listener = listener)



	track = ['okay', 'wow', 'the', 'this']
	stream.filter(track = track, languages = ['en'])
