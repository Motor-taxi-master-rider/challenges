import difflib
import re
import xml.etree.ElementTree
from collections import Counter

TOP_NUMBER = 10
RSS_FEED = 'rss.xml'
SIMILAR = 0.87


def get_tags():
    """Find all tags in RSS_FEED.
    Replace dash with whitespace."""
    with open(RSS_FEED) as fh:
        tree = xml.etree.ElementTree.parse(fh)
    return [re.sub(r'-+', ' ', node.text).lower() for node in tree.iter('category')]


def get_top_tags(tags):
    """Get the TOP_NUMBER of most common tags"""
    return Counter(tags).most_common(TOP_NUMBER)


def get_similarities(tags):
    """Find set of tags pairs with similarity ratio of > SIMILAR"""

    def match_similarity(origin_tag, match_tag):
        return difflib.SequenceMatcher(None, origin_tag, match_tag).ratio() >= SIMILAR

    tags = list(dict.fromkeys(tags))
    while tags:
        origin_tag = tags.pop()
        match_tags = [match_tag for match_tag in tags if match_similarity(origin_tag, match_tag)]
        if not match_tags:
            continue
        if len(match_tags) == 1:
            yield (origin_tag, match_tags[0])
        else:
            yield (origin_tag, match_tags)


if __name__ == "__main__":
    tags = get_tags()
    top_tags = get_top_tags(tags)
    print('* Top {} tags:'.format(TOP_NUMBER))
    for tag, count in top_tags:
        print('{:<20} {}'.format(tag, count))
    similar_tags = dict(get_similarities(tags))
    print()
    print('* Similar tags:')
    for singular, plural in similar_tags.items():
        print('{:<20} {}'.format(singular, plural))
