import re
import datetime
import feedparser
from time import mktime

from django.core.cache import cache


def fetch_activity(username='codeinthehole', cache_lifetime=3600):
    """
    Fetch latest activity from Github using the ATOM 
    feed for a user.
    """
    key = 'github_%s' % username
    activity = cache.get(key)
    if activity is None:
        activity = _fetch_github_activity(username)
        cache.set(key, activity, cache_lifetime)
    return activity

def _fetch_github_activity(username):
    url = 'https://github.com/%s.atom' % username
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        timestamp = mktime(entry['updated_parsed'])
        item = {'date_updated': datetime.datetime.fromtimestamp(timestamp),
                'summary': _anchorise_github_links(entry['summary'])}
        items.append(item)
    return items

_linkfinder = re.compile(r"\"/")

def _anchorise_github_links(text):
    return _linkfinder.sub(r'"https://github.com/', text)