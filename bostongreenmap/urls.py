from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from api.resources import ParkResource, \
    FacilityResource, \
    EntryResource, \
    NeighborhoodResource, \
    ActivityResource, \
    ParktypeResource, \
    ExploreParkResource, \
    ExploreFacilityResource, \
    ParkNameResource, \
    MBTAResource, \
    ExploreActivityResource, \
    FacilitytypeResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ActivityResource())
v1_api.register(EntryResource())
v1_api.register(ExploreActivityResource())
v1_api.register(ExploreFacilityResource())
v1_api.register(ExploreParkResource())
v1_api.register(FacilityResource())
v1_api.register(FacilitytypeResource())
v1_api.register(MBTAResource())
v1_api.register(NeighborhoodResource())
v1_api.register(ParkNameResource())
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
    # url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^my_profile/$', 'profiles.views.edit_profile', name='my_profile'),
    # url(r'^profiles/', include('profiles.urls')),
    url(r'^login_redirect/$', 'accounts.views.login_redirect',
        name='login_redirect'),

    url(r'^policy/$', 'parkmap.views.policy'),  # HOME
    url(r'^', include('parkmap.urls')),  # HOME

    # API
    (r'^api/', include(v1_api.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
