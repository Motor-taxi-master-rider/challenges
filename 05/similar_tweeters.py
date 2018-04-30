import csv
import os
import sys
from collections import namedtuple
from itertools import product

import spacy

DATA = 'data/'
Tweet = namedtuple('Tweet', ['id_str', 'created_at', 'text'])
nlp = spacy.load('en_core_web_lg')


def similar_tweeters(user1, user2):
    def filter_similar_tweet(tweets):
        global nlp
        tweet1, tweet2 = tweets
        tweet1, tweet2 = nlp(tweet1.text), nlp(tweet2.text)
        similarity = tweet1.similarity(tweet2)
        return similarity

    with open(os.path.join(DATA, f'{user1}.csv'), 'r', encoding='utf-8') as fh1, \
            open(os.path.join(DATA, f'{user2}.csv'), 'r', encoding='utf-8') as fh2:
        data1 = [Tweet(*row) for row in csv.reader(fh1)][1:]
        data2 = [Tweet(*row) for row in csv.reader(fh2)][1:]
        tweeter_similarity = sum(map(filter_similar_tweet, product(data1, data2))) / (len(data1) * len(data2))

    return tweeter_similarity


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: {} <user1> <user2>'.format(sys.argv[0]))
        sys.exit(1)

    user1, user2 = sys.argv[1:3]
    print(similar_tweeters(user1, user2))
