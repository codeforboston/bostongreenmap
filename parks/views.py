# Views for Parks
from django.core import urlresolvers
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings

import json
import logging
import itertools

from parks.models import Neighborhood, Park, Parkimage, Facility, Activity, Story


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
    featured_parks = Park.objects.filter(featured=True).prefetch_related('images')
    hero_images = Parkimage.objects.filter(hero_image=True)
    parks = Park.objects.distinct('name')
    
    hero_image_docs = []
    for i in hero_images:
        image_doc = i.get_thumbnail(include_large=True)
        if image_doc:
            hero_image_docs.append(image_doc)
    
    response = {
        'neighborhoods': [{'id': n.pk, 'name': n.name} for n in neighborhoods],
        'activities': [{'id': a.pk, 'name': a.name} for a in activities],
        'featured_parks': [{'id': a.pk, 'url': a.get_absolute_url(), 'name': a.name, 'description': a.description, 'images': a.get_image_thumbnails(include_large=False) } for a in featured_parks],
        'hero_images': hero_image_docs
    }
    return HttpResponse(json.dumps(response), mimetype='application/json')

def get_nearby_parks(request, park_id):
    """ Returns nearby parks as JSON
    """
    park = Park.objects.get(pk=park_id)
    nearby_parks = park.nearest_parks_by_distance(0.25).all()
    response = {
        'parks': [{'id': p.pk, 'name': p.name} for p in nearby_parks]
    }
    return HttpResponse(json.dumps(response), mimetype='application/json')


def get_recommended_parks(request, park_id):
    """ Returns recommended parks as JSON
    """
    park = Park.objects.get(pk=park_id)
    recommended_parks = park.recommended_parks()
    response = {
        'parks': [{'id': p.pk, 'name': p.name} for p in recommended_parks]
    }
    return HttpResponse(json.dumps(response), mimetype='application/json')


def get_featured_parks(request):
    """ Returns recommended parks as JSON
    """
    featured_parks = Park.objects.filter(featured=True).prefetch_related('images')
    response = {
        'featured_parks': [{'id': n.pk, 'name': n.name, 'image': n.thumbnail} for n in featured_parks]
    }
    return HttpResponse(json.dumps(response), mimetype='application/json')


def get_parks(request):
    """ Returns parks as JSON based search parameters
    """
    querydict = request.GET
    kwargs = querydict.dict()
    no_map = kwargs.pop('no_map', False)
    # FIXME: int() will throw if this arg isn't parseable. That should be handled
    page = int(kwargs.pop('page', 1))
    # FIXME: int() will throw if this arg isn't parseable. That should be handled
    # FIXME: We should figure out what a reasonable default is here.
    # *perhaps* we shouldn't do paging if `page` above is not specified?
    page_size = int(kwargs.pop('page_size', 15))
    user = request.user
    slug = kwargs.get('slug', False)

    filters = kwargs
    try:
        parks = Park.objects.filter(**filters).select_related('parkowner').distinct('name')
        parks_pages = Paginator(parks, page_size)
        parks_page = parks_pages.page(page)
        if no_map:
            parks_json = {p.pk: p.to_external_document(user, include_large=True, include_extra_info=bool(slug)) for p in parks_page}
            response_json = {
                "parks": parks_json,
                "pages": parks_pages.num_pages
            }
        else:
            # FIXME: should this even be paged? There's nowhere to put the total # of pages...
            response_json = {p.pk: p.to_external_document(user, include_large=True) for p in parks_page}

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
            activities = [a.name for a in f.activity.all()]
            geojson_prop = dict(
                name=f.name,
                icon=f.facilitytype.icon.url,
                activities=activities,
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
    coordinates = json.loads(park.geometry.geojson)
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

def park_ajax(request, park_slug):
    park = get_object_or_404(Park, slug=park_slug)
    stories = Story.objects.filter(park=park).order_by("-date")
    recommended_parks = [p.to_external_document(request.user) for p in park.recommended_parks()]
    park_as_json = {
        'detail': park.to_external_document(request.user),
        'recommended_parks': recommended_parks
    }
    return HttpResponse(json.dumps(park_as_json), mimetype='application/json')

