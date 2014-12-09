from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
admin.autodiscover()

from parks.views import HomePageView, BackboneHomePageView, HackathonHomePageView

admin.autodiscover()

urlpatterns = patterns('',

    # Home
    url(r'^$', HomePageView.as_view(), name='home'),

    # Backbone App
    url(r'^backbone', BackboneHomePageView.as_view(), name='backbone_home'),

    # Hackathon App
    url(r'^hackathon', HackathonHomePageView.as_view(), name='hackathon_home'),

    # Parks
    url(r'^parks/', include('parks.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # grappelli
    url(r'^grappelli/', include('grappelli.urls')),

)

if settings.DEBUG:
    static_view = never_cache(serve)
    
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', static_view, {
            'document_root': settings.STATIC_ROOT,
        }),url(r'^media/(?P<path>.*)$', static_view, {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
