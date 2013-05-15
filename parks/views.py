# Views for Parks
from django.core import serializers
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.utils.html import strip_tags
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext

from sorl.thumbnail import get_thumbnail

import json
import logging

from parks.models import Neighborhood, Park, Facility, Activity, Event, Parktype, Facilitytype


logger = logging.getLogger(__name__)

def get_topnav_data():
    """ Returns lists of all Neighborhoods, Activities and 
        Parks serialized as JSON.
    """
    neighborhoods = Neighborhood.objects.all().only('name')
    activities = Activity.objects.all().only('name')

    return neighborhoods, activities

def get_parks(request):
    """ Returns parks as JSON based search parameters
    """

    querydict = request.GET
    kwargs = querydict.dict()

    try:
        parks = Park.objects.filter(**kwargs).select_related('parkowner').prefetch_related('images')
        parks_json = dict()
        for p in parks:
            # embed all images
            # width: 270px
            images = []
            for i in p.images.all():
                try: 
                    tn = get_thumbnail(i.image, '250x250', crop='center', quality=80)
                    image = dict(
                        src=tn.url,
                        caption=strip_tags(i.caption),
                    )
                    images.append(image)
                except IOError, e:
                    logger.error(e)


            parks_json[p.pk] = dict(
                url=p.get_absolute_url(),
                name=p.name,
                description=p.description,
                images=images,
                access=p.get_access_display(),
                address=p.address,
                owner=p.parkowner.name,
            )
        return HttpResponse(json.dumps(parks_json), mimetype='application/json')

    except:
        # no content
        return HttpResponse(status=204)

def get_facilities(request, park_id):
    """ Returns facilities as JSON for park id
    """

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

        return context


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


