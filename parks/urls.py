from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('parks.views',
    # Examples:

    # returns park list
    url(r'^search/$', 'get_parks', name='get_parks'),

    # returns facilities
    url(r'^(?P<park_id>\d+)/facilities/$', 'get_facilities', name='get_facilities'),

    # park detail page
    url(r'^(?P<park_slug>[-\w]+)/$', 'parks_page', name='park'),
 
)
