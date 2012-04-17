from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass


class Park(models.Model):
    """
    Park or similar Open Space.
    """

    os_id = models.IntegerField('Park ID', primary_key=True, help_text='Refers to GIS OS_ID')
    name = models.CharField(max_length=100, blank=True, null=True)
    alt_name = models.CharField('Alternative name', max_length=100, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK to Neighborhood
    type = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK
    owner = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK
    friendsgroup = models.CharField(max_length=100, blank=True, null=True) #FIXME: FK
    access = models.CharField(max_length=10, blank=True, null=True) #FIXME: FK

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Park')
        verbose_name_plural = _('Parks')

    def __unicode__(self):
        return self.name


class Facility(models.Model):
    """
    Facility in or outside a park.
    """

    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK?
    activity = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK?
    location = models.CharField(max_length=50, blank=True, null=True, help_text='Address, nearby Landmark or similar location information.')
    status = models.CharField(max_length=50, blank=True, null=True) #FIXME: choices?
    park = models.ForeignKey(Park, blank=True, null=True)

    geometry = models.PointField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Facility')
        verbose_name_plural = _('Facilities')

    def __unicode__(self):
        return self.name


class Neighborhood(models.Model):
    """
    Neighborhood or town if no neighborhoods are available.
    """
    n_id = models.CharField('Neighborhood ID', max_length=20, help_text='ID derived from GIS, not necessarily unique since we are mixing neighborhood types.')
    name = models.CharField(max_length=50)

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Neighborhood')
        verbose_name_plural = _('Neighborhoods')

    def __unicode__(self):
        return self.name
    

