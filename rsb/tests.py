import httplib

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from rsb.models import Article

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
        