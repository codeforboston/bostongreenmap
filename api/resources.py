from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from bostonparks.tastyhacks import GeoResource, EncodedGeoResource
from parkmap.models import Neighborhood, Activity, Facility, Park, Parktype


class ParkResource(EncodedGeoResource):
    """
    Park
    """
    class Meta:
        queryset = Park.objects.transform(4326).all()
        allowed_methods = ['get',]
        filtering = {
            'name': ALL,
        }

class NeighborhoodResource(ModelResource):
    class Meta:
        queryset = Neighborhood.objects.all()
        allowed_methods = ['get']
        excludes = ['geometry', 'objects']
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(NeighborhoodResource, self).build_filters(filters)
        if  "activity" in filters:
            neighborhoods = get_neighborhoods(filters['activity'])
            queryset = Neighborhood.objects.filter(pk__in=neighborhoods)
            orm_filters = {"pk__in": [i for i in neighborhoods]}
        return orm_filters

class ParktypeResource(ModelResource):
    class Meta:
        queryset = Parktype.objects.all()
        allowed_methods = ['get']
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ParktypeResource, self).build_filters(filters)
        if  "neighborhood" in filters:
            parktypes = get_parktypes(filters['neighborhood'])
            queryset = Parktype.objects.filter(pk__in=parktypes)
            orm_filters = {"pk__in": [i for i in parktypes]}
        return orm_filters


class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        allowed_methods = ['get']
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ActivityResource, self).build_filters(filters)
        if  "neighborhood" in filters:
            activities = get_activities(filters['neighborhood'])
            queryset = Activity.objects.filter(pk__in=activities)
            orm_filters = {"pk__in": [i for i in activities]}
        return orm_filters

class EntryResource(ModelResource):
    neighborhood = fields.ForeignKey(NeighborhoodResource, 'neighborhood')
    activity = fields.ForeignKey(ActivityResource, 'activity')
    parktype = fields.ForeignKey(ParktypeResource, 'parktype')
    class Meta:
        queryset = Neighborhood.objects.all()
        allowed_methods = ['get']

def get_neighborhoods(activity_slug):
    """
    Get all Neighborhood ids that have an activity.
    """
    activity = Activity.objects.get(slug=activity_slug)
    parks = [fac.park for fac in Facility.objects.filter(activity=activity) if fac.park]
    neighborhoods = []
    for p in parks:
        neighborhoods.extend(p.neighborhoods.all())
    return list(set([n.id for n in neighborhoods]))

def get_parktypes(neighborhood_slug):
    """
    Get all Neighborhood ids that have an activity.
    """
    neighborhood = Neighborhood.objects.get(slug=neighborhood_slug)
    parks = Park.objects.filter(neighborhoods=neighborhood)
    parktypes = []
    for park in parks:
        parktypes.append(park.parktype.id)

    return list(set(parktypes))



def get_activities(neighborhood_slug):
    """
    Get all activitty ids that are in a neighborhood.
    """
    neighborhood = Neighborhood.objects.get(slug=neighborhood_slug)
    parks = Park.objects.filter(geometry__intersects=neighborhood.geometry)
    facilities = []
    for park in parks:
        facilities.extend(park.facility_set.all())
    activities = []
    for fac in facilities:
        activities.extend(fac.activity.all())
    return list(set([a.id for a in activities]))
