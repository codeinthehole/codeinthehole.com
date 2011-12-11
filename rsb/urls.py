from django.conf.urls.defaults import *

from rsb.views import ArticleListView, ArticleDetailView, AboutView, \
                      ProjectsView, TalksView, ArticleTagView, HomeView, \
                      ArticleRedirectView, ArticlesFeedView

urlpatterns = patterns('',
    # Static pages
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    # Blog pages
    url(r'^articles/$', ArticleListView.as_view(), name='articles'),
    url(r'^articles/feed/$', ArticlesFeedView(), name='articles-feed'),
    url(r'^articles/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article'),
    url(r'^articles/tagged/(?P<name>[.\w-]+)/$', ArticleTagView.as_view(), name='tagged'),
    # Redirects from old site
    url(r'^archives/(?P<id>\d+)-.*$', ArticleRedirectView.as_view(), name='article-redirect'),
)
