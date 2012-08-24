from django.contrib.gis.db import models

# Create your models here.



class MBTAStop(models.Model):
    stop_id = models.CharField(max_length=256)
    stop_code = models.CharField(max_length=256)
    stop_name = models.CharField(max_length=256)
    stop_desc = models.CharField(max_length=256)
    zone_id = models.CharField(max_length=256)
    stop_url = models.CharField(max_length=256)
    location_type = models.CharField(max_length=256)
    parent_station = models.CharField(max_length=256)
    #lat_long = models.PointField(blank=True, null=True,srid=4326)
    lat_long = models.PointField(blank=True, null=True,srid=26986)
    objects = models.GeoManager()
