from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('parks.views',
    # Examples:

    # returns park list
    url(r'^search/$', 'get_parks', name='get_parks'),
    
    # returns list of all neighborhood names and ids and activity names and ids
    url(r'^get_neighborhoods_and_activities_list/$', 'get_neighborhoods_and_activities_list', name='get_neighborhoods_and_activities_list'),

    #latest image
    url(r'^get_latest_picture/$', 'get_latest_picture', name='get_latest_picture'),

    # featured parks
    url(r'^get_featured_parks/$', 'get_featured_parks', name='get_featured_parks'),

    # returns facilities
    url(r'^(?P<park_id>\d+)/facilities/$', 'get_facilities', name='get_facilities'),

    # park detail page
    url(r'^(?P<park_slug>[-\w]+)/$', 'park_ajax', name='park'),

    # nearby parks
    url(r'^(?P<park_id>\d+)/nearby_parks/$', 'get_nearby_parks', name='get_nearby_parks'),

    # recommended parks
    url(r'^(?P<park_id>\d+)/recommended_parks/$', 'get_recommended_parks', name='get_recommended_parks'),


)


