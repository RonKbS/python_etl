import os
import json
from datetime import datetime, timedelta

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
pd = os.environ.get('DB_PASSWORD')

df1 = pd.DataFrame(columns = ['date', 'tweet'])
df2 = pd.DataFrame(columns = ['date', 'tweet'])
now = datetime.now()

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
				# connect(username, created_at, tweet, retweet_count, place, location)
				df1.concat(pd.DataFrame([created_at, tweet], ignore_index=True))
				print("Tweet colleted at: {} ".format(str(created_at)))

				if datetime.now() - now == timedelta(minutes=1):
					now = datetime.now()
					data = TweetObject().clean_tweets(df1)
					data['Sentiment'] = np.array(
						[TweetObject().sentiment(x) for x in data['clean_tweets']]
					)
					df1.iloc[0:0]

					pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] > 0]
					neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] < 0]
					neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] == 0]

					print("percentage of positive tweets: {}%".format(100*(len(pos_tweets)/len(data['clean_tweets']))))
					print("percentage of negative tweets: {}%".format(100*(len(neg_tweets)/len(data['clean_tweets']))))
					print("percentage of neutral tweets: {}%".format(100*(len(neu_tweets)/len(data['clean_tweets']))))

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
