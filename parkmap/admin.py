from django.contrib.gis import admin

from parkmap.models import Facility, Neighborhood, Park, Activity, Event, Parktype, Parkowner, Facilitytype


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000  
admin.GeoModelAdmin.default_zoom = 12

class FacilityAdmin(admin.OSMGeoAdmin):
    list_display = ['name','activity_string','facilitytype','parktype_string']
    list_filter = ('activity', )



class LookupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    list_editable = ['name',]


#admin.site.register(Greenspace, admin.OSMGeoAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Facilitytype, LookupAdmin)
admin.site.register(Park, admin.OSMGeoAdmin)
admin.site.register(Parktype, LookupAdmin)
admin.site.register(Parkowner, LookupAdmin)
admin.site.register(Neighborhood, admin.OSMGeoAdmin)
admin.site.register(Activity, LookupAdmin)
admin.site.register(Event)
