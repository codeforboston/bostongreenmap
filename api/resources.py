from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
import datetime
from tastypie import fields
from sorl.thumbnail import get_thumbnail



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
            if filters['activity'] == 'all':
                neighborhoods = Neighborhood.objects.all()
            else:
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

class FacilitytypeResource(ModelResource):
    class Meta:
        queryset = Facilitytype.objects.all()
        allowed_methods = ['get']
        cache = SimpleCache()
        filtering = {
            'id': ALL,
            'name': ALL,
        }


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
            'id': ALL,
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

        if "id_list" in filters:
            id_list  = filters['id_list'].split(",")
            orm_filters = {"pk__in": [i for i in id_list]}
            return orm_filters

        if "facilitytypes" in filters and "neighborhoods" in filters:
            fts = filters['facilitytypes'].split(",")
            facilities = Facility.objects.filter(facilitytype__in=fts).select_related()
            park_facility_ids = [f.park.id for f in facilities if f.park]

            if not facilities:
                return {'pk__in':[]}

            if filters['neighborhoods'] == "all":
                parks = Park.objects.filter(pk__in=park_facility_ids)
            else:
                neighborhoods = Neighborhood.objects.get(id=filters['neighborhoods'])
                parks = Park.objects.filter(pk__in=park_facility_ids, neighborhoods=neighborhoods)

            if parks:
                orm_filters = {"pk__in": [p.id for p in parks]}
                return orm_filters
            return {'pk__in':[]}

        if "neighborhood" in filters and \
           "activity" in filters:
            parks = filter_play_park(filters)
            if parks:
                orm_filters = {"pk__in": [p.id for p in parks]}
            return orm_filters

        if "neighborhood" in filters and \
           "parktype" in filters and \
           "activity_ids" in filters:
            parks = filter_explore_park(filters)
            orm_filters = {"pk__in": [i.id for i in parks]}
            return orm_filters
        return orm_filters

    def dehydrate(self, bundle):
        bundle.obj.geometry.transform(4326)
        bundle.data['lat_long'] = bundle.obj.lat_long()
        bundle.data['thumb'] = bundle.obj.parkimage_thumb()
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
    facilitytype = fields.ToOneField(FacilitytypeResource, 'facilitytype')

    class Meta:
        queryset = Facility.objects.transform(4326).filter(park__isnull=False).order_by('id')
        allowed_methods = ['get', ]
        resource_name = 'facility'
        cache = SimpleCache()
        filtering = {
            'name': ALL,
            'park': ALL_WITH_RELATIONS,
            'activity': ALL_WITH_RELATIONS,
            'facilitytype': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        desc = bundle.obj.park.description
        if desc and  len(desc.split()) > 10:
            desc = " ".join(desc.split()[:10]) + "..."
        else: 
            desc=""
        bundle.data['description'] = desc
        bundle.data['notes'] = bundle.obj.notes
        bundle.data['access'] = bundle.obj.access
        bundle.data['park_slug'] = bundle.obj.park.slug
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(FacilityResource, self).build_filters(filters)

        if "facilitytypes" in filters and "park" in filters:
            fts = filters['facilitytypes'].split(",")
            facilities = Facility.objects.filter(facilitytype__in=fts, park=filters['park'])
            if facilities:
                orm_filters = {"pk__in": [f.id for f in facilities]}

        return orm_filters

class ExploreActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        allowed_methods = ('get',)
        cache = SimpleCache()
        excludes = ('status', 'location')

    def build_filters(self, filters=None):
        print "HERE"
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
            orm_filters = {"pk__in": [i.id for i in parks]}
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
            orm_filters = {"pk__in": [i.id for i in parks]}
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
    if neighborhood_id == 'all':
        activities = Activity.objects.all()
    else:
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
    if filters['neighborhood'] == 'all':
        neighborhood = Neighborhood.objects.all()
    else:
        neighborhood = Neighborhood.objects.get(id=filters['neighborhood'])
    activities = Activity.objects.filter(id=filters['activity'])
    facilities = Facility.objects.filter(activity=activities)
    try:
        park_facility_ids = [f.park.id for f in facilities if f.park]
    except AttributeError:  ## should we return a 404 here?
        return []
    if filters['neighborhood'] == 'all':
        parks = Park.objects.filter(pk__in=park_facility_ids)
    else:
        parks = Park.objects.filter(pk__in=park_facility_ids, neighborhoods=neighborhood)
    return parks
