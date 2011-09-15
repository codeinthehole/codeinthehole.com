from django.conf.urls.defaults import *

from cb.views import ArticleListView, ArticleDetailView, AboutView, ProjectsView, TalksView

urlpatterns = patterns('',
    # Static pages
    url(r'^$', ArticleListView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^projects/$', ProjectsView.as_view(), name='projects'),
    url(r'^talks/$', TalksView.as_view(), name='talks'),
    # Blog pages
    url(r'^articles/$', ArticleListView.as_view(), name='articles'),
    url(r'^article/(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article'),
)
