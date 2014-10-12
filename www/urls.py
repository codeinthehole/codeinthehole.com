from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.views import generic
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'^cv/', generic.TemplateView.as_view(
        template_name='cv.html'), name="cv"),
    url(r'^oscar/', generic.TemplateView.as_view(
        template_name='oscar.html'), name="oscar"),
    (r'', include('rsb.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        (r'^404.html', generic.TemplateView.as_view(template_name='404.html')),
        (r'^500.html', generic.TemplateView.as_view(template_name='500.html')),
    )
