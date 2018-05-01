import json
import sys
import time

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

from config import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET

MAX_TWEETS = 1000
OUTPUT = 'data_{}.json'.format(int(time.time()))


class MyListener(StreamListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def on_data(self, data):
        try:
            with open(OUTPUT, 'a') as f:
                f.write(data + '\n')
                self.count += 1
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        if self.count >= MAX_TWEETS:
            return False
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    keywords_and = ' '.join(sys.argv[1:])

    twitter_stream = Stream(auth=auth, listener=MyListener())
    twitter_stream.filter(track=keywords_and)
