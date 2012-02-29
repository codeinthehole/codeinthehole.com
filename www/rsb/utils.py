import re
import datetime
import requests
import simplejson as json

from django.core.cache import cache


def fetch_tweets(username='codeinthehole'):
    """
    Return tweets but with caching
    """
    key = 'tweets_%s' % username
    tweets = cache.get(key)
    if tweets is None:
        tweets = _fetch_tweets(username)
        cache.set(key, tweets, 300)
    return tweets


def _fetch_tweets(username='codeinthehole'):
    """
    Return a list of tweets for a given user
    """
    url = "https://twitter.com/statuses/user_timeline.json?screen_name=%s" % username
    response = requests.get(url)
    raw_tweets = json.loads(response.content)
    if 'error' in raw_tweets:
        return []
    processed_tweets = []
    for tweet in raw_tweets:
        # Ignore replies
        if tweet['text'].startswith('@'):
            continue
        data = {
            'text': htmlify(tweet['text']),
            'date_created': datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")}
        processed_tweets.append(data)
    return processed_tweets


urlfinder = re.compile(r"(https?://[^ ]+)")
tweeterfinder = re.compile(r"@(\w+)")


def anchorise_urls(text):
    return urlfinder.sub(r'<a href="\1">\1</a>', text)


def anchorise_twitter_user_refs(text):
    return tweeterfinder.sub(r'<a href="http://twitter.com/\1">@\1</a>', text)
    

def htmlify(text):
    return anchorise_twitter_user_refs(anchorise_urls(text))
    