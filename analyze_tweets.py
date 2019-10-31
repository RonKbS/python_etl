import os
import re

import mysql.connector
import pandas as pd
import nltk
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from mysql.connector import Error
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



class TweetObject():

    def __init__(self, host, database, user):
        self.password = os.environ.get('DB_PASSWORD')
        self.host = host
        self.database = database
        self.user = user

    def MySQLConnect(self, query):

        try:
            con = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8'
            )

            if con.is_connected():
                print("Successfully connected to database")

                cursor = con.cursor()
                query = query

                cursor.execute(query)
                data = cursor.fetchall()

				# store in dataframe
                df = pd.DataFrame(data,columns = ['date', 'tweet'])

        except:
            raise 


        cursor.close()
        con.close()

        return df

    def clean_tweets(self, df):
        # text processing
        stopword_list = stopwords.words('english')
        wordnet_lemmatizer = WordNetLemmatizer()
        df['clean_tweets'] = None
        df['len'] = None

        for i in range(0, len(df['tweet'])):
            # remove none letters
            exclusion_list = ['[^a-zA-Z]','rt', 'http', 'co', 'RT']
            exclusions = '|'.join(exclusion_list)
            text = re.sub(exclusions, ' ', df['tweet'][i])
            text = text.lower()
            words = text.split()
            words = [wordnet_lemmatizer.lemmatize(word) for word in words if not word in stopword_list]
            df['clean_tweets'][i] = ' '.join(words)

        # Create column with data length
        df['len'] = np.array([len(tweet) for tweet in data["clean_tweets"]])

        return df


    def sentiment(self, tweet):

        analysis = TextBlob(tweet)

        if analysis.sentiment.polarity > 0:
            return 1

        elif analysis.sentiment.polarity == 0:
            return 0

        else:
            return -1


    def save_to_csv(self, df):

        try:
            df.to_csv("clean_tweets.csv")
            print("\n")
            print("csv successfully saved. \n")

        except Error as e:
            print(e)



if __name__ == '__main__':

    t = TweetObject( host='localhost', database='tweet', user='root')

    data  = t.MySQLConnect("SELECT created_at, tweet FROM `tweet`.`tweets`;")
    data = t.clean_tweets(data)

    data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])

	# t.word_cloud(data)
    t.save_to_csv(data)


    pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] > 0]
    neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] < 0]
    neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] == 0]


	#Print results

    print("percentage of positive tweets: {}%".format(100*(len(pos_tweets)/len(data['clean_tweets']))))
    print("percentage of negative tweets: {}%".format(100*(len(neg_tweets)/len(data['clean_tweets']))))
    print("percentage of neutral tweets: {}%".format(100*(len(neu_tweets)/len(data['clean_tweets']))))
