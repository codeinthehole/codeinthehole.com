import re
import datetime
import feedparser
from time import mktime

from cacheback.decorators import cacheback


@cacheback(60 * 15, fetch_on_miss=False)
def fetch_activity(username, num_items=None):
    url = 'https://github.com/%s.atom' % username
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        timestamp = mktime(entry['updated_parsed'])
        item = {'date_updated': datetime.datetime.fromtimestamp(timestamp),
                'summary': _anchorise_github_links(entry['summary'])}
        items.append(item)
    if num_items is not None:
        return items[:num_items]
    return items


_linkfinder = re.compile(r"\"/")


def _anchorise_github_links(text):
    return _linkfinder.sub(r'"https://github.com/', text)