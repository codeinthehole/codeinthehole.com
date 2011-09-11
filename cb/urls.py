from django.conf.urls.defaults import *

from cb.views import ArticleListView, ArticleDetailView, AboutView

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^articles/$', ArticleListView.as_view(), name='articles'),
    url(r'^article/(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='article'),
)
