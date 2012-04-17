from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass


class Greenspace(models.Model):
    """
    Park or similar Greenspace.
    """

    name = models.CharField(max_length=100)
    alt_name = models.CharField('Alternative name', max_length=100)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50) #FIXME: FK
    type = models.CharField(max_length=50) #FIXME: FK
    owner = models.CharField(max_length=50) #FIXME: FK
    friendsgroup = models.CharField(max_length=100) #FIXME: FK
    access = models.CharField(max_length=10) #FIXME: FK

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Greenspace')
        verbose_name_plural = _('Greenspaces')

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
    green_space = models.IntegerField(blank=True, null=True) # FIXME: FK to Greenspace

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
    n_id = models.CharField('Neighborhood ID', max_length=20, help_text='ID derived from GIS, not necessarily unique.')
    name = models.CharField(max_length=50)

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Neighborhood')
        verbose_name_plural = _('Neighborhoods')

    def __unicode__(self):
        return self.name
    

