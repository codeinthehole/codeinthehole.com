from django.conf.urls.defaults import *
from django.views.generic import RedirectView
from django.contrib.sitemaps import Sitemap

from rsb.views import ArticleListView, ArticleDetailView, AboutView, \
                      ArticleTagView, HomeView, \
                      ArticleRedirectView, ArticlesFeedView
from rsb.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.date_published


sitemaps = {'articles': ArticleSitemap}


urlpatterns = patterns('',
    # Static pages
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    # Blog pages
    url(r'^writing/$', ArticleListView.as_view(), name='articles'),
    url(r'^writing/feed/$', ArticlesFeedView(), name='articles-feed'),
    url(r'^writing/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article'),
    url(r'^writing/tagged/(?P<name>[ .\w-]+)/$', ArticleTagView.as_view(), name='tagged'),
    # Feeds
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    # Redirects from old site
    url(r'^archives/(?P<id>\d+)-.*$', ArticleRedirectView.as_view(), name='article-redirect'),
    url(r'^tutorials/thesisfile/', RedirectView.as_view(url='/writing/writing-a-thesis-in-latex/')),
    url(r'^tutorials/cgl/(?P<file>\w+)$', RedirectView.as_view(url='/static/tutorial/%(file)s')),
    url(r'^rss.php', RedirectView.as_view(url='/writing/feed/')),
    url(r'^feeds/', RedirectView.as_view(url='/writing/feed/')),
    url(r'^my/', RedirectView.as_view(url='/about/')),
    url(r'^categories/', RedirectView.as_view(url='/writing/')),
    url(r'^plugin/', RedirectView.as_view(url='/writing/')),
)
