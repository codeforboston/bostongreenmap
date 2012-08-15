from django.contrib.gis import admin

from parkmap.models import Facility, Neighborhood, Park, Activity, Event, Parktype, Parkowner, Facilitytype, Friendsgroup, Story
from sorl.thumbnail import default
ADMIN_THUMBS_SIZE = '150'


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000
admin.GeoModelAdmin.default_zoom = 11


class ParkAdmin(admin.OSMGeoAdmin):
    list_display = ['name', 'parkowner','park_image_thumb' ]
    list_filter = ('neighborhoods', )
    search_fields = ['name']

    def park_image_thumb(self, obj):
         if obj.image:
             thumb = default.backend.get_thumbnail(obj.image.file, ADMIN_THUMBS_SIZE)
             return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
         else:
             return "No Image" 
    park_image_thumb.short_description = 'Park Image'
    park_image_thumb.allow_tags = True

    readonly_fields = ['park_image_thumb',]



class FacilityAdmin(admin.OSMGeoAdmin):
    search_fields = ['name', 'park__name']
    exclude = ('park',)
    list_display = ['name', 'activity_string', 'facilitytype', 'parktype_string']
    list_filter = ('activity', )


class LookupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_editable = ['name', ]


#admin.site.register(Greenspace, admin.OSMGeoAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Facilitytype, LookupAdmin)
admin.site.register(Park, ParkAdmin)
admin.site.register(Parktype, LookupAdmin)
admin.site.register(Parkowner, LookupAdmin)
admin.site.register(Neighborhood, admin.OSMGeoAdmin)
admin.site.register(Activity, LookupAdmin)
admin.site.register(Event)
admin.site.register(Friendsgroup)
admin.site.register(Story)
