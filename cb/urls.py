from django.conf.urls.defaults import *

from cb.views import ArticleListView

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view(), name='article-list'),
)
