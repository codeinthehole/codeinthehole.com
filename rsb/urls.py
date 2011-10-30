from django.conf.urls.defaults import *

from rsb.views import ArticleListView, ArticleDetailView, AboutView, \
                      ProjectsView, TalksView, ArticleTagView, HomeView

urlpatterns = patterns('',
    # Static pages
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^projects/$', ProjectsView.as_view(), name='projects'),
    url(r'^talks/$', TalksView.as_view(), name='talks'),
    # Blog pages
    url(r'^articles/$', ArticleListView.as_view(), name='articles'),
    url(r'^articles/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article'),
    url(r'^articles/tagged/(?P<name>[\w-]+)/$', ArticleTagView.as_view(), name='tagged'),
)
