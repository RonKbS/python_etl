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



