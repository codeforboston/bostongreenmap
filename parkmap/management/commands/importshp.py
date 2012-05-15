import os

from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping

from parkmap.models import Park, Facility, Neighborhood


class Command(BaseCommand):
    args = 'facilities parks neighborhoods'
    help = 'Imports facilities.shp, parks.shp or neighborhoods.shp form the data directory.'

    config = {
        'facilities': {
            'file': 'data/facilities.shp',
            'model': Facility,
            'mapping': {
                'name': 'Name',
                'facilitytype_legacy': 'Type',
                'activity_legacy': 'Activity',
                'location': 'Location',
                'status': 'Status',
                'geometry': 'POINT',
            }
        },
        'parks': {
            'file': 'data/parks.shp',
            'model': Park,
            'mapping': {
                'os_id': 'OS_ID',
                'name': 'NAME',
                'alt_name': 'ALT_NAME',
                'address': 'Address',
                'phone': 'Phone',
                'access': 'Access',
                'geometry': 'MULTIPOLYGON',
            }
        },
        'neighborhoods': {
            'file': 'data/neighborhoods.shp',
            'model': Neighborhood,
            'mapping': {
                'n_id': 'n_id',
                'name': 'name',
                'geometry': 'MULTIPOLYGON',
            }
        }
    }

    def handle(self, *args, **options):
        for shp in args:
            lm = LayerMapping(self.config[shp]['model'], self.config[shp]['file'], self.config[shp]['mapping'], 
                encoding='iso-8859-1')
            lm.save(strict=True, verbose=True)

            self.stdout.write('Successfully imported "%s"\n' % shp)
