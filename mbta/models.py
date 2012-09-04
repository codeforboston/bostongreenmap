from django.contrib.gis.db import models

# Create your models here.



class MBTAStop(models.Model):  # Stops.csv
    stop_id = models.CharField(max_length=256)
    stop_code = models.CharField(max_length=256)
    stop_name = models.CharField(max_length=256)
    stop_desc = models.CharField(max_length=256)
    zone_id = models.CharField(max_length=256)
    stop_url = models.TextField()
    location_type = models.CharField(max_length=256)
    parent_station = models.CharField(max_length=256)
    lat_long = models.PointField(blank=True, null=True,srid=26986)
    objects = models.GeoManager()  # required for anything special like  __distance_gt


# ALL FILES LOCATED IN /home/django/MBTA_DATA

class MBTAAgency(models.Model):
    agency_id = models.CharField(max_length=256)
    agency_name = models.CharField(max_length=256)
    agency_url = models.TextField()
    agency_timezone = models.CharField(max_length=256)
    agency_lang = models.CharField(max_length=2)
    agency_phone = models.CharField(max_length=16)
#
class MBTACalendar(models.Model):
    service_id = models.CharField(max_length=256)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
#
#class MBTACalendarDate(models.Model):
#    service_id
#    date
#    exception_type
#
class MBTACFeedInfo(models.Model):
    feed_publisher_name = models.CharField(max_length=256)
    feed_publisher_url = models.TextField()
    feed_lang  = models.CharField(max_length=2)
    feed_start_date = models.DateField()
    feed_end_date = models.DateField()
    feed_version = models.CharField(max_length=256)
#
class MBTAFrequencies(models.Model):
    trip_id = models.CharField(max_length=256)
    start_time = models.TimeField()
    end_time = models.TimeField()
    headway_secs = models.IntegerField()
#
#class MBTARoutes(models.Model):
#    route_id = models.CharField(max_length=256)
#    agency_id = models.CharField(max_length=256)
#    route_short_name
#    route_long_name
#    route_desc
#    route_type
#    route_url
#    route_color
#    route_text_color
#
#class MBTAShapes(models.Model):
#    shape_id
#    shape_pt_lat
#    shape_pt_lon
#    shape_pt_sequence
#    shape_dist_traveled
#
#class MBTAStopTimes(models.Model):
#    trip_id
#    arrival_time
#    departure_time
#    stop_id
#    stop_sequence
#    stop_headsign
#    pickup_type
#    drop_off_type
#
#class MBTATransfers(models.Model):
#    from_stop_id
#    to_stop_id
#    transfer_type
#    min_transfer_time
#
#class MBTATrips(models.Model):
#    route_id
#    service_id
#    trip_id
#    trip_headsign
#    direction_id
#    block_id
#    shape_id
