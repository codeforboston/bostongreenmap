from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('parkmap.views',
    # Examples:

    url(r'^park/play/$', 'play_page', name='play'),  # B  (Detail)
    url(r'^explore/$', 'explore', name='explore'),  # Explore
    url(r'^park/(?P<park_slug>[-\w]+)/$', 'parks_page', name='park'),  # B  (Detail)
    url(r'^event/(?P<event_name>[-\w]+)/(?P<event_id>[-\w]+)/$', 'events', name='events'),  # B  (Detail)

    url(r'^neighborhood/(?P<n_slug>[-\w]+)/$', 'neighborhood', name='neighborhood_parks'),  # A
    url(r'^plan/$', 'plan_a_trip', name='plan_a_trip'),  # A

    url(r'^neighborhood/(?P<n_slug>[-\w]+)/(?P<a_slug>[-\w]+)/$',
        'parks_in_neighborhood_with_activities',
         name='neighborhood_activities'),  # C

    url(r'^ajax/(?P<n_slug>[-\w]+)/(?P<a_slug>[-\w]+)/$', 'neighborhood_activity_ajax', name='neighborhood_actity_ajax'),  # HOME
    url(r'^$', 'home_page', name='home'),  # HOME

)
