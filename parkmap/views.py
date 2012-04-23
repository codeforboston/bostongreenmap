# Views for Parkmap

from django.shortcuts import (render_to_response, get_object_or_404,
                              get_list_or_404, redirect)
from django.http import HttpResponse
from datetime import datetime
from parkmap.models import Neighborhood, Park, Facility, Activity, Event
from django.template.defaultfilters import slugify

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

#Temporary view to see Parks page
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
    neighborhood = get_object_or_404(Neighborhood,slug=n_slug)
    activity = get_object_or_404(Activity,slug=a_slug)
    facility = Facility.objects.filter(activity=activity)
    facility_ids = []
    for f in facility:
       facility_ids.append(f.id)
    parks = Park.objects.filter(neighborhood=neighborhood,facility__id__in=facility_ids)


    response_d = {
        'neighborhood':neighborhood,
        'parks':parks}
    return render_to_response('parkmap/neighborhood.html',response_d)
    

def events(request,event_id,event_name):
    event = get_object_or_404(Event,pk=event_id)
    return render_to_response('parkmap/event.html',{'event':event})

