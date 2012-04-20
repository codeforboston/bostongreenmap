from django.contrib.gis import admin

from parkmap.models import Facility,Neighborhood, Park, Activity, Event


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000  
admin.GeoModelAdmin.default_zoom = 12


#admin.site.register(Greenspace, admin.OSMGeoAdmin)
admin.site.register(Facility, admin.OSMGeoAdmin)
admin.site.register(Park, admin.OSMGeoAdmin)
admin.site.register(Neighborhood, admin.OSMGeoAdmin)
admin.site.register(Activity)
admin.site.register(Event)
