import re
import datetime
import simplejson as json

import requests
import twitter
from django.conf import settings
from cacheback.decorators import cacheback


@cacheback(10 * 60, fetch_on_miss=False)
def fetch_tweets(username='codeinthehole'):
    """
    Return a list of tweets for a given user
    """
    api = twitter.Api(
        consumer_key=settings.TWITTER_CONSUMER_KEY,
        consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
    statuses = api.GetUserTimeline()

    processed_tweets = []
    for tweet in statuses:
        # Ignore replies
        if tweet.text.startswith('@'):
            continue
        data = {
            'text': htmlify(tweet.text),
            'date_created': datetime.datetime.strptime(
                tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")}
        processed_tweets.append(data)
    return processed_tweets


urlfinder = re.compile(r"(https?://[^ )\n]+)", re.MULTILINE)
tweeterfinder = re.compile(r"@(\w+)", re.MULTILINE)
hashtagfinder = re.compile(r"#(\w+)", re.MULTILINE)


def linebreaks(text):
    return text.replace('\n', '<br />');


def anchorise_urls(text):
    return urlfinder.sub(r'<a class="tweet_url" href="\1">\1</a>', text)


def anchorise_twitter_user_refs(text):
    return tweeterfinder.sub(r'<a href="http://twitter.com/\1">@\1</a>', text)


def anchorise_twitter_hashtags(text):
    return hashtagfinder.sub(
        r'<a href="http://twitter.com/#!/search/%23\1">#\1</a>', text)


def htmlify(text):
    filters = [anchorise_urls,
               anchorise_twitter_user_refs,
               anchorise_twitter_hashtags,
               linebreaks]
    output = text
    for fn in filters:
        output = fn(output)
    return output
