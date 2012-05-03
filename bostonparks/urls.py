from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api.resources import ParkResource, EntryResource, NeighborhoodResource, ActivityResource, ParktypeResource
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(NeighborhoodResource())
v1_api.register(ActivityResource())
v1_api.register(EntryResource())
v1_api.register(ParkResource())
v1_api.register(ParktypeResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bostonparks.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/django/webapps/static/'}),

    url(r'^', include('parkmap.urls')),  # HOME

    # API
    (r'^api/', include(v1_api.urls)),
)
