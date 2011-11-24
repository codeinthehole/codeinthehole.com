import httplib

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from rsb.models import Article
from rsb.utils import fetch_tweets, htmlify

def create_article(filename="sample.rst", title="sample title", summary="sample summary",
                   body_rst="", body_html="", **kwargs):
    """
    Create an article with the passed params
    """
    return Article.objects.create(filename=filename, title=title, summary=summary, 
                                  body_rst=body_rst, body_html=body_html, **kwargs)


class ArticleModelTests(TestCase):
    
    def test_is_published(self):
        article = create_article()
        self.assertFalse(article.is_published)
        
        
class ArticleViewsTests(TestCase):
    
    def test_single_article_view(self):
        article = create_article()
        url = reverse('article', kwargs={'slug': article.slug})
        response = Client().get(url)
        self.assertEqual(httplib.OK, response.status_code)
        
        
class TwitterTests(TestCase):
    
    def test_list_is_returned(self):
        results = fetch_tweets()
        self.assertTrue(len(results) > 0)
        
    tests = (
        ('http://t.co/QwAiDgq9 - Just some Lego heads from Reddit',
         '<a href="http://t.co/QwAiDgq9">http://t.co/QwAiDgq9</a> - Just some Lego heads from Reddit'),
        ('Impressed by python\'s requests library - almost too easy: http://t.co/EBGJXJoP',
         'Impressed by python\'s requests library - almost too easy: <a href="http://t.co/EBGJXJoP">http://t.co/EBGJXJoP</a>'),
        ('@old_sound Yes, definitely.',
         '<a href="http://twitter.com/old_sound">@old_sound</a> Yes, definitely.')     
    )    
        
    def test_htmlify_converts_normal_links(self):
        for raw, expected in self.tests: 
            self.assertEquals(expected, htmlify(raw))
        