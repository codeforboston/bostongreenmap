from django.contrib.gis.db import models
from django.db import IntegrityError
import re
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass



class Event(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) 
    slug = models.SlugField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.name

    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Event, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break



class Park(models.Model):
    """
    Park or similar Open Space.
    """

    os_id = models.IntegerField('Park ID', primary_key=True, help_text='Refers to GIS OS_ID')
    name = models.CharField(max_length=100, blank=True, null=True) 
    slug = models.SlugField(max_length=100, blank=True, null=True)
    alt_name = models.CharField('Alternative name', max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    neighborhood = models.ManyToManyField("Neighborhood")
    type = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK
    owner = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK
    friendsgroup = models.CharField(max_length=100, blank=True, null=True) #FIXME: FK
    events = models.ManyToManyField("Event",blank=True,null=True)
    access = models.CharField(max_length=10, blank=True, null=True) #FIXME: FK
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    #activity = models.ManyToManyField("Activity")   #Not allowing an Activity without a Facility in a park.

    class Meta:
        verbose_name = _('Park')
        verbose_name_plural = _('Parks')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('park', [slugify(self.name)])
    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Park, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break

class Activity(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
    def __unicode__(self):
        return self.name


    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Activity, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
        
class Facility(models.Model):
    """
    Facility in or outside a park.
    """

    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True) #FIXME: FK?
    activity = models.ManyToManyField("Activity")   #FIXME: FK?
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

    def save(self, *args, **kwargs):
        try:
            # cache containing park
            self.park = Park.objects.get(geometry__contains=self.geometry)
        except:
            self.park = None       
 
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Facility, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
        super(Facility, self).save(*args, **kwargs)

        
    @models.permalink
    def get_absolute_url(self):
        return ('facility', [slugify(self.name)])

       


class Neighborhood(models.Model):
    """
    Neighborhood or town if no neighborhoods are available.
    """
    n_id = models.CharField('Neighborhood ID', max_length=20, help_text='ID derived from GIS, not necessarily unique since we are mixing neighborhood types.')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Neighborhood')
        verbose_name_plural = _('Neighborhoods')

    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('neighborhood', [slugify(self.name)])

    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        
        while True:
            try:
                super(Neighborhood, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
    

