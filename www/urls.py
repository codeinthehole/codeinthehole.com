from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include('rsb.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^500.html', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        (r'^404.html', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
    )
