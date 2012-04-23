# Views for Parkmap
import json

from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404, redirect)
from django.http import HttpResponse,Http404
from datetime import datetime
from parkmap.models import Neighborhood, Park, Facility, Activity, Event
from django.template.defaultfilters import slugify

#Temporary view to see Play page
def play_page(request):
    return render_to_response('parkmap/play.html')  


def get_list():
    # Query each of the three classes.
    parks = Park.objects.all()
    facilities = Facility.objects.all()
    neighborhoods = Neighborhood.objects.all()
    return parks,facilities,neighborhoods

#Home page
def home_page(request):
    parks, facilities, neighborhoods = get_list()   
    activities = Activity.objects.all()
    return render_to_response('parkmap/home.html',{
        'parks':parks,
        'facilities':facilities,
        'activities':activities,
        'neighborhoods':neighborhoods,
    })

def parks_page(request,park_slug):
    park = get_object_or_404(Park,slug=park_slug)
    return render_to_response('parkmap/park.html',
        {'park':park}
    )

def neighborhood(request,n_slug): # Activity slug, and Neighborhood slug 
    neighborhood = Neighborhood.objects.get(slug=n_slug)
    parks = Park.objects.filter(neighborhood=neighborhood)
    response_d = {
        'neighborhood':neighborhood,
        'parks':parks}
    return render_to_response('parkmap/neighborhood.html',response_d)

def parks_in_neighborhood_with_activities(request,a_slug,n_slug): # Activity slug, and Neighborhood slug 
    neighborhood,parks = get_n_p_with_a(n_slug,a_slug)
    response_d = {
        'neighborhood':neighborhood,
        'parks':parks}
    return render_to_response('parkmap/neighborhood.html',response_d)

def get_n_p_with_a(n_slug,a_slug):
    """
    Get parks in a neighborhood that have the specific activity for any of its facilities
    if no request is passed, returns neighborhood and the parks
    """
    n = get_object_or_404(Neighborhood,slug=n_slug)
    a = get_object_or_404(Activity,slug=a_slug)
    fac = Facility.objects.filter(activity=a)
    facility_ids = []
    for f in fac:
       facility_ids.append(f.id)
    p = Park.objects.filter(neighborhood=n,facility__id__in=facility_ids)
    return n,p

def neighborhood_activity_ajax(request,n_slug,a_slug):
    """
    Returns a json string of parks with activities in the specified neighborhood
    """
    try:
        n,parks = get_n_p_with_a(n_slug,a_slug)
    except Http404:
        return HttpResponse("{}")
    parks_json = []
    for park in parks:
        p_dict = {}
        p_dict['activity'] = []
        for f in park.facility_set.all():
            for a in f.activity.all():
                p_dict['activity'].append({'slug':a.slug})
        p_dict['name'] = park.name
        p_dict['slug'] = park.slug
        p_dict['description'] = park.description
        parks_json.append(p_dict)
    
    return HttpResponse(parks_json)
    
    
    
    
def events(request,event_id,event_name):
    event = get_object_or_404(Event,pk=event_id)
    return render_to_response('parkmap/event.html',{'event':event})


