from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from bostonparks.tastyhacks import GeoResource, EncodedGeoResource
from parkmap.models import Park


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