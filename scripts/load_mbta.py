"""
    Run this in the shell to import the Stop CSV files.
"""

LAT_LONG = 4326 # Magic Geographical numbers  This one is Latitude and Longitude
BOSTON = 26986 # Magic Geographical numbers  This one is Boston Area coordinates


def load_stops():
    import csv
    from mbta.models import MBTAStop
    from django.contrib.gis.geos import *
    headers = ["stop_id","stop_code","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url","location_type","parent_station"]
    with open('/home/django/MBTA_DATA/stops.csv', 'rb') as f:
        junk = f.next()
        reader = csv.reader(f)
        for row in reader:
            d_row = {}
            for i,val in enumerate(row):
               d_row[headers[i]] = val
            x = 'SRID=%s;POINT(%s %s)' % (LAT_LONG, d_row['stop_lon'], d_row['stop_lat'])
            p = GEOSGeometry(x)
            stop = MBTAStop.objects.get_or_create(lat_long=p, stop_id=d_row['stop_id'])
            p.transform(BOSTON) # Transform to this so that we can use in the boston area.
            stop.lat_long = p
            stop.stop_id = d_row['stop_id']
            stop.stop_code = d_row['stop_code']
            stop.stop_name = d_row['stop_name']
            stop.stop_desc = d_row['stop_desc']
            stop.zone_id = d_row['zone_id']
            stop.stop_url = d_row['stop_url']
            stop.location_type = d_row['location_type']
            stop.parent_station = d_row['parent_station']
            stop.save()
