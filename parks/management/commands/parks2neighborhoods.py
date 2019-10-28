import os

from django.core.management.base import BaseCommand

from parks.models import Park, Neighborhood


class Command(BaseCommand):
    help = 'Assigns intersecting neighborhoods to parks.'

    def handle(self, *args, **options):
        parks = Park.objects.all()
        for park in parks:
            neighborhoods = Neighborhood.objects.filter(geometry__intersects=park.geometry)
            park.neighborhoods.clear()
            park.neighborhoods.add(*neighborhoods)
            self.stdout.write('Updated "%s"\n' % park.name)
