# Views for Parks
from django.core import urlresolvers
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.utils.html import strip_tags
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings

from sorl.thumbnail import get_thumbnail

import json
import logging
import itertools

from parks.models import Neighborhood, Park, Facility, Activity, Event, Parktype, Facilitytype


logger = logging.getLogger(__name__)

def get_topnav_data():
    """ Returns lists of all Neighborhoods, Activities and 
        Parks serialized as JSON.
    """
    neighborhoods = Neighborhood.objects.all().only('name')
    activities = Activity.objects.all().only('name')

    return neighborhoods, activities

def get_neighborhoods_and_activities_list(request):
    neighborhoods = Neighborhood.objects.all()
    activities = Activity.objects.all()
    response = {
        'neighborhoods': [{'id': n.pk, 'name': n.name} for n in neighborhoods],
        'activities': [{'id': a.pk, 'name': a.name} for a in activities]
    }
    return HttpResponse(json.dumps(response), mimetype='application/json')

def get_parks(request):
    """ Returns parks as JSON based search parameters
    """
    print "got here"
    querydict = request.GET
    kwargs = querydict.dict()
    no_map = kwargs.pop('no_map', False)
    user = request.user

    filters = kwargs
    try:
        parks = Park.objects.filter(**filters).select_related('parkowner').prefetch_related('images')
        if no_map:
            parks_json = { p.pk: p.to_external_document(user, include_large=True) for p in parks }
            carousel = []
            if not filters:
                # gets up to ten images if parks have images
                carousel = list(itertools.islice([
                    dict(p.get('images')[0].items() + {'url': p.get('url')}.items())
                    for key, p in parks_json.iteritems()
                    if any(p.get('images'))
                ],
                0, 10))
            response_json = {
                "parks": parks_json,
                "carousel": carousel
            }
        else:
            response_json = { p.pk: p.to_external_document(user) for p in parks }


        return HttpResponse(json.dumps(response_json), mimetype='application/json')

    except Exception as e:
        # no content
        print e
        return HttpResponse(str(e), status=204)

def get_facilities(request, park_id):
    """ Returns facilities as JSON for park id
    """

    user = request.user

    try:
        park = Park.objects.get(pk=park_id)
        facilities = Facility.objects.transform(4326).filter(park=park).select_related('facilitytype').prefetch_related('activity') 
        features = []
        for f in facilities:
            activities = [ a.name for a in f.activity.all() ]
            geojson_prop = dict(
                name=f.name,
                icon=f.facilitytype.icon.url,
                activities = activities,
                status=f.status,
                access=f.access,
                notes=f.notes,
            )
            if user.has_perm('parks.change_facility'):
                geojson_prop['change_url'] = urlresolvers.reverse('admin:parks_facility_change', args=(f.id,))
            geojson_geom = json.loads(f.geometry.geojson)
            geojson_feat = dict(type='Feature', geometry=geojson_geom, properties=geojson_prop)
            features.append(geojson_feat)
        response = dict(type='FeatureCollection', features=features)
        return HttpResponse(json.dumps(response), mimetype='application/json')

    except:
        # no content
        return HttpResponse(status=204)


class HomePageView(TemplateView):

    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['neighborhoods'], context['activities'] = get_topnav_data()
        context['ga_tracking_id'] = getattr(settings, 'GA_TRACKING_ID', '')
        context['uservoice_forum_id'] = getattr(settings, 'USERVOICE_FORUM_ID', '')

        return context

class BackboneHomePageView(TemplateView):
    template_name = 'base_backbone.html'

class HackathonHomePageView(TemplateView):
    template_name = 'base_redevelop.html'

class NeighborhoodParkListView(ListView):

    context_object_name = 'park_list'
    template_name = 'parks/neighborhood.html'

    def get_queryset(self):
        self.neighborhood = get_object_or_404(Neighborhood, slug=self.kwargs['slug'])
        return Park.objects.filter(neighborhoods=self.neighborhood)

    def get_context_data(self, **kwargs):
        context = super(NeighborhoodParkListView, self).get_context_data(**kwargs)
        context['neighborhood'] = self.neighborhood
        return context


def parks_page(request, park_slug):
    park = get_object_or_404(Park, slug=park_slug)
    encoder = cgpolyencode.GPolyEncoder()
    coordinates = simplejson.loads(park.geometry.geojson)
    map = encoder.encode(coordinates['coordinates'][0][0])
    stories = Story.objects.filter(park=park).order_by("-date")
    #stops = MBTAStop.objects.filter(lat_long__distance_lte=(park.geometry.centroid,D(mi=settings.MBTA_DISTANCE))) # this distance doesn't overload the page with a million stops.
    
    neighborhoods, activities = get_topnav_data()
    print "park %s" % park
    print "neighborhoods %s" % neighborhoods
    print "activities %s" % activities
    if request.method == 'POST':
        story = Story()
        f = StoryForm(request.POST, instance=story)
        if f.is_valid():
            story.park = park
            f.save()
            f = StoryForm()
    else:
        f = StoryForm()
    return render_to_response('parks/park.html',
        {'park': park,
         'map': map,
         #'stops': stops,
         'story_form': f,
         'stories': stories,
         'request': request,
         'acres': park.geometry.area * 0.000247,
         'neighborhoods': neighborhoods,
         'activities': activities,
        },
        context_instance=RequestContext(request)
    )


