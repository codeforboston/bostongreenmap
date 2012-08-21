# Views for Parkmap
from django.contrib.sites.models import Site

import json
from django.utils import simplejson
from django.core.mail import send_mail

from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from parkmap.models import Neighborhood, Park, Facility, Activity, Event, Parktype, Story, Facilitytype
from forms import StoryForm
from django.template import RequestContext
from django.conf import settings


import cgpolyencode
current_site = Site.objects.get_current()

#Temporary view to see Play page
def play_page(request):
    neighborhoods = Neighborhood.objects.all().order_by('name')
    activities = Activity.objects.all().order_by('name')
    response_d = {
        'neighborhoods': neighborhoods,
        'activities': activities,
        }

    return render_to_response('parkmap/play.html', response_d,
        context_instance=RequestContext(request))


def get_list():
    # Query each of the three classes.
    parks = Park.objects.all()
    facilities = Facility.objects.all()
    neighborhoods = Neighborhood.objects.all().order_by('name')
    return parks, facilities, neighborhoods


#Home page
def home_page(request):
    parks, facilities, neighborhoods = get_list()
    all_parks = Park.objects.all().order_by('name')
    activities = Activity.objects.all()
    stories = Story.objects.all().order_by('-date')[:6]
    return render_to_response('parkmap/home.html', {
        'parks': parks,
        'all_parks': all_parks,
        'facilities': facilities,
        'activities': activities,
        'neighborhoods': neighborhoods,
        'stories':stories,
        }, context_instance=RequestContext(request))


def parks_page(request, park_slug):
    park = get_object_or_404(Park, slug=park_slug)
    encoder = cgpolyencode.GPolyEncoder()
    coordinates = simplejson.loads(park.geometry.geojson)
    map = encoder.encode(coordinates['coordinates'][0][0])
    stories = Story.objects.filter(park=park).order_by("-date")
    if request.method == 'POST':
        story = Story()
        f = StoryForm(request.POST, instance=story)
        if f.is_valid():
            story.park = park
            f.save()
            f = StoryForm()
    else:
        f = StoryForm()
            
    return render_to_response('parkmap/park.html',
        {'park': park,
         'map': map,
         'story_form': f,
         'stories': stories,
         'acres': park.geometry.area * 0.000247,
        },
        context_instance=RequestContext(request)
    )


def neighborhood(request, n_slug):  # Activity slug, and Neighborhood slug
    neighborhood = Neighborhood.objects.get(slug=n_slug)
    parks = Park.objects.filter(neighborhoods=neighborhood)
    response_d = {
        'neighborhood': neighborhood,
        'parks': parks,
        }
    return render_to_response('parkmap/neighborhood.html',
        response_d,
        context_instance=RequestContext(request)
    )


def parks_in_neighborhood_with_activities(request, a_slug, n_slug):  # Activity slug, and Neighborhood slug
    activities = Activity.objects.all()
    activity = Activity.objects.get(slug=a_slug)
    neighborhood, parks = get_n_p_with_a(n_slug, a_slug)
    response_d = {
        'neighborhood': neighborhood,
        'activities': activities,
        'activity': activity,
        'a_slug': a_slug,
        'parks': parks}
    return render_to_response('parkmap/play.html',
        response_d,
        context_instance=RequestContext(request)
)


def get_n_p_with_a(n_slug, a_slug):
    """
    Get parks in a neighborhood that have the specific activity for any of its facilities
    if no request is passed, returns neighborhood and the parks
    """
    a = get_object_or_404(Activity, slug=a_slug)
    fac = Facility.objects.filter(activity=a)
    if n_slug == 'all':
        n = Neighborhood.objects.all()
    else:
        n = get_object_or_404(Neighborhood, slug=n_slug)
    facility_ids = []
    for f in fac:
        facility_ids.append(f.id)
    p = Park.objects.filter(neighborhoods=n, facility__id__in=facility_ids)
    return n, p


def neighborhood_activity_ajax(request, n_slug, a_slug):
    """
    Returns a json string of parks with activities in the specified neighborhood
    """
    try:
        n, parks = get_n_p_with_a(n_slug, a_slug)
    except Http404:
        return HttpResponse("{}")
    parks_json = []
    for park in parks:
        p_dict = {}
        p_dict['activity'] = []
        for f in park.facility_set.all():
            for a in f.activity.all():
                p_dict['activity'].append({'slug': a.slug})
        p_dict['name'] = park.name
        p_dict['slug'] = park.slug
        p_dict['description'] = park.description
        parks_json.append(p_dict)

    return HttpResponse(json.dumps(parks_json))


def events(request, event_id, event_name):
    event = get_object_or_404(Event, pk=event_id)
    return render_to_response('parkmap/event.html', {'event': event})


def explore(request):  # Activity slug, and Neighborhood slug
    parkname = request.POST.get('parkname',None)
    neighborhoods = Neighborhood.objects.all().order_by('name')
    #activities = Activity.objects.all().order_by('name')
    parks = Park.objects.all().order_by('name')
    facilitytypes = Facilitytype.objects.all().order_by('name')
    neighborhood_slug = request.GET.get('neighborhood', None)
    neighborhood = None
    if neighborhood_slug:
        neighborhood = Neighborhood.objects.get(slug=neighborhood_slug)
    response_d = {
        'neighborhoods': neighborhoods,
        'neighborhoodpassed': neighborhood,
        'facilitytypes':facilitytypes,
        'parks':parks,
        'parkname':parkname,
        }
    return render_to_response('parkmap/explore.html',
        response_d,
        context_instance=RequestContext(request)
        )


def plan_a_trip(request):  # Activity slug, and Neighborhood slug
    
    return render_to_response('parkmap/trip.html',
        { },
        context_instance=RequestContext(request)
        )

    
def story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    return render_to_response('parkmap/story.html',
        dict(story=story), context_instance=RequestContext(request))


def story_flag(request,story_id):
    story = Story.objects.get(pk=story_id)
    if not story.objectionable_content:
        MESSAGE = """
A user of the Boston Parks website has flagged this story as objectionable.

Here is the story:
{story}

Link to Admin: http://{domain}/admin/parkmap/story/{id}
""".format(story=story.text,domain=current_site.domain,id=story.id)
        emails = []
        for admin in settings.ADMINS:
            emails.append(admin[1])
        send_mail('Flagged Story on the BostonParks website', MESSAGE, 'support@bostonparks.org',
                emails, fail_silently=False)
        story.objectionable_content = True
        story.save()
    return HttpResponse("")
   
def policy(request):
    return render_to_response('parkmap/policy.html',
        {}, context_instance=RequestContext(request))
