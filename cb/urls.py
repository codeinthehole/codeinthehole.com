from django.conf.urls.defaults import *

from cb.views import ArticleListView, ArticleDetailView

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view(), name='article-list'),
    url(r'^article/(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='article-detail'),
)
