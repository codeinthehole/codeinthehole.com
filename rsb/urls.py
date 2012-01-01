from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from rsb.views import ArticleListView, ArticleDetailView, AboutView, \
                      ProjectsView, TalksView, ArticleTagView, HomeView, \
                      ArticleRedirectView, ArticlesFeedView

urlpatterns = patterns('',
    # Static pages
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    # Blog pages
    url(r'^writing/$', ArticleListView.as_view(), name='articles'),
    url(r'^writing/feed/$', ArticlesFeedView(), name='articles-feed'),
    url(r'^writing/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article'),
    url(r'^writing/tagged/(?P<name>[.\w-]+)/$', ArticleTagView.as_view(), name='tagged'),
    # Redirects from old site
    url(r'^archives/(?P<id>\d+)-.*$', ArticleRedirectView.as_view(), name='article-redirect'),
    url(r'^tutorials/thesisfile/', redirect_to, {'url': '/writing/writing-a-thesis-in-latex/'}),
)
