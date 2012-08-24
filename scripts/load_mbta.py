"""
    Run this in the shell to import the Stop CSV files.
"""


def load_stops():
    import csv
    from mbta.models import MBTAStop
    from django.contrib.gis.geos import *
    headers = ["stop_id","stop_code","stop_name","stop_desc","stop_lat","stop_lon","zone_id","stop_url","location_type","parent_station"]
    with open('/home/django/stops.csv', 'rb') as f:
        junk = f.next()
        reader = csv.reader(f)
        for row in reader:
            d_row = {}
            for i,val in enumerate(row):
               d_row[headers[i]] = val
            stop = MBTAStop()
            x = 'SRID=%s;POINT(%s %s)' % (4326, d_row['stop_lon'], d_row['stop_lat'])
            p = GEOSGeometry(x)
            p.transform(26986) # Transform to this so that we can use in the boston area.
    
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
