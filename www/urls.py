from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'', include('rsb.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    from django.views import generic
    urlpatterns += patterns('',
        (r'^404.html', generic.TemplateView.as_view(template_name='404.html')),
        (r'^500.html', generic.TemplateView.as_view(template_name='500.html')),
    )
