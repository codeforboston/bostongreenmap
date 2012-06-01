from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
from tastypie import fields

from api.tastyhacks import EncodedGeoResource, GeoResource
from parkmap.models import Neighborhood, Activity, Facility, Park, Parktype, Facilitytype


class NeighborhoodResource(ModelResource):
    class Meta:
        queryset = Neighborhood.objects.all()
        allowed_methods = ['get']
        excludes = ['geometry', 'objects']
        cache = SimpleCache()
        filtering = {
            'slug': ALL,
            'id': ALL,
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(NeighborhoodResource, self).build_filters(filters)
        if  "activity" in filters:
            neighborhoods = get_neighborhoods(filters['activity'])
            queryset = Neighborhood.objects.filter(pk__in=neighborhoods)
            orm_filters = {"pk__in": [i.id for i in queryset]}
        return orm_filters

class ParktypeResource(ModelResource):
    class Meta:
        queryset = Parktype.objects.all()
        allowed_methods = ['get']
        cache = SimpleCache()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ParktypeResource, self).build_filters(filters)
        if  "neighborhood" in filters:
            parktypes = get_parktypes(filters['neighborhood'])
            queryset = Parktype.objects.filter(pk__in=parktypes)
            orm_filters = {"pk__in": [i.id for i in queryset]}
        return orm_filters


class ParkResource(EncodedGeoResource):
    """
    Park with enocoded geometries
    """

    neighborhoods = fields.ManyToManyField(NeighborhoodResource, 'neighborhoods')
    parktype = fields.ToOneField(ParktypeResource, 'parktype')

    class Meta:
        queryset = Park.objects.transform(4326).filter(parktype__isnull=False)
        allowed_methods = ['get', ]
        resource_name = 'park'
        cache = SimpleCache()
        filtering = {
            'os_id': ALL,
            'name': ALL,
            'slug': ALL,
            'area': ALL,
            'neighborhoods': ALL_WITH_RELATIONS,
            'parktype': ALL_WITH_RELATIONS,
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ParkResource, self).build_filters(filters)
        if "neighborhood" in filters and \
           "activity" in filters:
            parks = filter_play_park(filters)
            if parks:
                orm_filters = {"pk__in": [p.os_id for p in parks]}
        if "neighborhood" in filters and \
           "parktype" in filters and \
           "activity_ids" in filters:
            parks = filter_explore_park(filters)
            orm_filters = {"pk__in": [i.os_id for i in parks]}
        return orm_filters

    def dehydrate(self, bundle):
        bundle.obj.geometry.transform(4326)
        bundle.data['lat_long'] = bundle.obj.lat_long()
        return bundle


class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        allowed_methods = ['get']
        limit = queryset.count()
        cache = SimpleCache()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ActivityResource, self).build_filters(filters)
        if  "neighborhood" in filters:
            activities = get_activities(filters['neighborhood'])
            queryset = Activity.objects.filter(pk__in=activities)
            orm_filters = {"pk__in": [i.id for i in queryset]}
        return orm_filters


class FacilityResource(GeoResource):
    """
    Facility as GeoJSON objects
    """

    park = fields.ToOneField(ParkResource, 'park')
    icon = fields.CharField(attribute='icon_url')
    activity = fields.ManyToManyField(ActivityResource, 'activity')
    activity_string = fields.CharField(attribute='activity_string')
    admin_url = fields.CharField(attribute='admin_url')

    class Meta:
        queryset = Facility.objects.transform(4326).filter(park__isnull=False)
        allowed_methods = ['get', ]
        resource_name = 'facility'
        cache = SimpleCache()
        filtering = {
            'name': ALL,
            'park': ALL_WITH_RELATIONS,
            'activity': ALL_WITH_RELATIONS,
        }

class ExploreActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        allowed_methods = ('get',)
        cache = SimpleCache()
        excludes = ('status', 'location')

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ExploreActivityResource, self).build_filters(filters)
        if "neighborhood" in filters and "parktype" in filters:
            activities = filter_explore_activity(filters)
            orm_filters = {"pk__in": [i.id for i in activities]}
        return orm_filters


class ExploreParkResource(EncodedGeoResource):
    class Meta:
        queryset = Park.objects.transform(4326).all()
        allowed_methods = ('get',)
        cache = SimpleCache()
        excludes = ('status', 'location')

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ExploreParkResource, self).build_filters(filters)
        if "neighborhood" in filters and \
           "parktype" in filters and \
           "activity_ids" in filters:
            parks = filter_explore_park(filters)
            orm_filters = {"pk__in": [i.os_id for i in parks]}
        return orm_filters

class ParkNameResource(EncodedGeoResource):
    class Meta:
        queryset = Park.objects.transform(4326).all()
        allowed_methods = ('get',)
        cache = SimpleCache()
        excludes = ('status', 'location')
        filtering = {
            'name': ALL,
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ParkNameResource, self).build_filters(filters)
        if "name" in filters:
            parks = Park.objects.filter(name__icontains=filters['name'])
            orm_filters = {"pk__in": [i.os_id for i in parks]}
        return orm_filters


class ExploreFacilityResource(GeoResource):

    icon = fields.CharField(attribute='icon_url')
    activity_string = fields.CharField(attribute='activity_string')
    admin_url = fields.CharField(attribute='admin_url')

    class Meta:
        queryset = Facility.objects.transform(4326).all()
        allowed_methods = ('get',)
        cache = SimpleCache()
        excludes = ('status', 'location')

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ExploreFacilityResource, self).build_filters(filters)
        if "neighborhood" in filters and \
           "parktype" in filters and \
           "activity_ids" in filters:
            facilities = filter_explore_facility(filters)
            orm_filters = {"pk__in": [i.id for i in facilities]}
        return orm_filters


class EntryResource(ModelResource):
    neighborhood = fields.ForeignKey(NeighborhoodResource, 'neighborhood')
    activity = fields.ForeignKey(ActivityResource, 'activity')
    parktype = fields.ForeignKey(ParktypeResource, 'parktype')
    explorepark = fields.ForeignKey(ExploreParkResource, 'explorepark')
    playpark = fields.ForeignKey(ParkResource, 'playpark')
    explorefacility = fields.ForeignKey(ExploreFacilityResource, 'explorefacility')
    exploreactivity = fields.ForeignKey(ExploreActivityResource, 'exploreactivity')
    parkname = fields.ForeignKey(ParkNameResource, 'parkname')

    class Meta:
        queryset = Neighborhood.objects.all()
        allowed_methods = ['get']
        cache = SimpleCache()


## Indepth filter functions
def get_neighborhoods(activity_id):
    """
    Get all Neighborhood ids that have an activity.
    """
    activity = Activity.objects.get(id=activity_id)
    parks = [fac.park for fac in Facility.objects.filter(activity=activity) if fac.park]
    neighborhoods = []
    for p in parks:
        neighborhoods.extend(p.neighborhoods.all())
    return list(set([n.id for n in neighborhoods]))


def get_parktypes(neighborhood_id):
    """
    Get all Neighborhood ids that have an activity.
    """
    neighborhood = Neighborhood.objects.get(id=neighborhood_id)
    parks = Park.objects.filter(neighborhoods=neighborhood)
    parktypes = []
    for park in parks:
        if (filter_explore_activity({'neighborhood': neighborhood_id, 'parktype': park.parktype.id})):
            parktypes.append(park.parktype.id)
    return list(set(parktypes))


def get_activities(neighborhood_id):
    """
    Get all activitty ids that are in a neighborhood.
    """
    neighborhood = Neighborhood.objects.get(id=neighborhood_id)
    parks = Park.objects.filter(geometry__intersects=neighborhood.geometry)
    facilities = []
    for park in parks:
        facilities.extend(park.facility_set.all())
    activities = []
    for fac in facilities:
        activities.extend(fac.activity.all())
    return list(set([a.id for a in activities]))


def filter_explore_park(filters):
    neighborhood = Neighborhood.objects.get(id=filters['neighborhood'])
    parktype = Parktype.objects.get(pk=filters['parktype'])
    activity_pks = filters['activity_ids'].split(",")
    activities = Activity.objects.filter(pk__in=activity_pks)
    parks = Park.objects.filter(neighborhoods=neighborhood, parktype=parktype)
    facilities = Facility.objects.filter(park__in=parks)
    parks_filtered = []
    for facility in facilities:
        for activity in activities:
            if activity in facility.activity.all():
                parks_filtered.append(facility.park)
    return parks_filtered


def filter_explore_activity(filters):
    neighborhood = Neighborhood.objects.get(id=filters['neighborhood'])
    parktype = Parktype.objects.get(pk=filters['parktype'])
    parks = Park.objects.filter(neighborhoods=neighborhood, parktype=parktype)
    facilities = Facility.objects.filter(park__in=parks)
    activities = []
    for facility in facilities:
        activities.extend(facility.activity.all())
    return list(set(activities))


def filter_explore_facility(filters):
    neighborhood = Neighborhood.objects.get(id=filters['neighborhood'])
    parktype = Parktype.objects.get(pk=filters['parktype'])
    activity_pks = filters['activity_ids'].split(",")
    activities = Activity.objects.filter(pk__in=activity_pks)
    parks = Park.objects.filter(neighborhoods=neighborhood, parktype=parktype)
    facilities = Facility.objects.filter(park__in=parks)
    facilities_filtered = []
    for facility in facilities:
        for activity in activities:
            if activity in facility.activity.all():
                facilities_filtered.append(facility)
    return facilities_filtered


def filter_play_park(filters):
    neighborhood = Neighborhood.objects.get(id=filters['neighborhood'])
    activities = Activity.objects.filter(id=filters['activity'])
    facilities = Facility.objects.filter(activity=activities)
    try:
        park_facility_ids = [f.park.os_id for f in facilities]
    except AttributeError:
        return []
    parks = Park.objects.filter(pk__in=park_facility_ids, neighborhoods=neighborhood)
    return parks
