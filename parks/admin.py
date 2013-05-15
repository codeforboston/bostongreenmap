from django.contrib.gis import admin

from parks.models import Facility, Neighborhood, Park, Activity, Event, Parktype, Parkowner, Parkimage, Facilitytype, Friendsgroup, Story
from sorl.thumbnail import default
from django.conf import settings

# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7912100
admin.GeoModelAdmin.default_lat = 5210000
admin.GeoModelAdmin.default_zoom = 11


class ParkAdmin(admin.OSMGeoAdmin):
    list_display = ['name', 'parkowner' ]
    list_filter = ('neighborhoods', )
    search_fields = ['name']
    exclude = ('slug', )

    def park_image_thumb(self, obj):
         if obj.image:
             thumb = default.backend.get_thumbnail(obj.image.file, settings.ADMIN_THUMBS_SIZE)
             return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
         else:
             return "No Image" 
    park_image_thumb.short_description = 'Park Image'
    park_image_thumb.allow_tags = True

    readonly_fields = ['park_image_thumb',]



class FacilityAdmin(admin.OSMGeoAdmin):
    search_fields = ['name', 'park__name']
    exclude = ('park',)
    list_display = ['pk', 'name', 'activity_string', 'facilitytype', ]
    list_editable = ['name', 'facilitytype', ]
    list_filter = ('activity', )


class LookupAdmin(admin.ModelAdmin):

    def ic(self, obj):
        if hasattr(obj, 'icon'):
            thumb = default.backend.get_thumbnail(obj.icon.file,"24")
            return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
        else:
            return ""

    ic.short_description = 'Park Image'
    ic.allow_tags = True

    list_display = ['id', 'name','ic' ]
    list_editable = ['name', ]


class ParkimageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'thumbnail', 'caption', ]
    list_editable = ['caption', ]
    search_fields = ['caption', ]
    readonly_fields = ('thumbnail',)
    list_per_page = 20


#admin.site.register(Greenspace, admin.OSMGeoAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Facilitytype, LookupAdmin)
admin.site.register(Park, ParkAdmin)
admin.site.register(Parktype, LookupAdmin)
admin.site.register(Parkowner, LookupAdmin)
admin.site.register(Parkimage, ParkimageAdmin)
admin.site.register(Neighborhood, admin.OSMGeoAdmin)
admin.site.register(Activity, LookupAdmin)
admin.site.register(Event)
admin.site.register(Friendsgroup)
admin.site.register(Story)
