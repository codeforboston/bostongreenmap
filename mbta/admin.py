from django.contrib.gis import admin
from mbta.models import MBTAStop
# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000
admin.GeoModelAdmin.default_zoom = 11

class MBTAStopAdmin(admin.OSMGeoAdmin):
    list_display = ['stop_id','stop_name']
admin.site.register(MBTAStop, MBTAStopAdmin)
                                          
