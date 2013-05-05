import re
import datetime
import requests
import simplejson as json

from cacheback.decorators import cacheback


@cacheback(10 * 60, fetch_on_miss=False)
def fetch_tweets(username='codeinthehole'):
    """
    Return a list of tweets for a given user
    """
    url = "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s"
    response = requests.get(url % username)
    if response.status_code != 200:
        raise RuntimeError("Unable to fetch tweets")
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
            'date_created': datetime.datetime.strptime(
                tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")}
        processed_tweets.append(data)
    return processed_tweets


urlfinder = re.compile(r"(https?://[^ )]+)")
tweeterfinder = re.compile(r"@(\w+)")
hashtagfinder = re.compile(r"#(\w+)")


def linebreaks(text):
    return text.replace('\n', '<br />');


def anchorise_urls(text):
    return urlfinder.sub(r'<a href="\1">\1</a>', text)


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
