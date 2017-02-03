from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import matplotlib.pyplot as plt
#Tanner's keys
consumer_key = 'tgxm3fkzxyyWFvEwFppZrsN3p'
consumer_secret = 'R4OGuyMn0XppBmahsDvcuqrwnCykyh7JCRmxBTlhhzw6RZTJ9Z'
access_token = 	'2618989681-qPyR0RumhmSADd4nJ5b70IudMY7v8ipE0a934OB'
access_token_secret = '17K3QALr7gxfG5oVIecuAL93oGqRCalu7TzLqPY45ltTT'

class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

def main():
     #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
    tweets_data_path = '../data/twitter_data.txt'

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue

if __name__ == '__main__':
    main()
