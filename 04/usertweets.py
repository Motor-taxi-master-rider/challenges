import csv
import os
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import tweepy

from config import ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

Tweet = namedtuple('Tweet', 'id_str created_at text')


class UserTweets(object):
    def __init__(self, handle, max_id=None):
        """Get handle and optional max_id.
        Use tweepy.OAuthHandler, set_access_token and tweepy.API
        to create api interface.
        Use _get_tweets() helper to get a list of tweets.
        Save the tweets as data/<handle>.csv"""
        time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.output_file = os.path.join(DEST_DIR, f'{handle}_{time}.{EXT}')
        self._handle = handle
        self._max_id = max_id
        self._tweets = list(self._get_tweets())
        self._save_tweets()

    def _get_tweets(self):
        """Hint: use the user_timeline() method on the api you defined in init.
        See tweepy API reference: http://docs.tweepy.org/en/v3.5.0/api.html
        Use a list comprehension / generator to filter out fields
        id_str created_at text (optionally use namedtuple)"""
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        for tweet in api.user_timeline(self._handle, count=NUM_TWEETS, max_id=self._max_id):
            yield Tweet(id_str=tweet.id_str, created_at=tweet.created_at, text=tweet.text.replace('\n', ' '))

    def _save_tweets(self):
        """Use the csv module (csv.writer) to write out the tweets.
        If you use a namedtuple get the column names with Tweet._fields.
        Otherwise define them as: id_str created_at text
        You can use writerow for the header, writerows for the rows"""

        with open(self.output_file, 'w', encoding='utf-8', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerow(Tweet._fields)
            for tweet in self._tweets:
                writer.writerow(tweet)

    def __len__(self):
        """See http://pybit.es/python-data-model.html"""
        return len(self._tweets)

    def __getitem__(self, pos):
        """See http://pybit.es/python-data-model.html"""
        return self._tweets[pos]


if __name__ == "__main__":
    twitter_users = ('pybites', 'izzy_spideypool', 'bbelderbos')
    with ThreadPoolExecutor(max_workers=3) as executor:
        wait_for = [executor.submit(UserTweets, handle) for handle in twitter_users]
        for future in as_completed(wait_for):
            user = future.result()
            print('--- {} ---'.format(user._handle))
            for tw in user[:5]:
                print(tw)
            print()
