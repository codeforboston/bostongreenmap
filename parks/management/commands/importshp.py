import os

from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping

from parks.models import Park, Facility, Neighborhood


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
            'file': 'fixtures/shp/quincy_parks.shp',
            'model': Park,
            'mapping': {
                'os_id': 'os_id',
                'name': 'Quinc_Name',
                'geometry': 'MULTIPOLYGON',
            }
        },
        'neighborhoods': {
            'file': 'fixtures/shp/quincy.shp',
            'model': Neighborhood,
            'mapping': {
                'n_id': 'n_id',
                'name': 'name',
                'slug': 'slug',
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
