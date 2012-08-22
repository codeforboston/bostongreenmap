from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.db.utils import IntegrityError
from django.db import transaction
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import get_thumbnail, default



import re

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
        """
        Auto-populate an empty slug field from the MyModel name and
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
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('neighborhood', [slugify(self.name)])

    def save(self, *args, **kwargs):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """

        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        super(Neighborhood, self).save(*args, **kwargs)


class Parktype(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _('Parktype')
        verbose_name_plural = _('Parktypes')

    def __unicode__(self):
        return self.name


class Parkowner(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _('Parkowner')
        verbose_name_plural = _('Parkowners')

    def __unicode__(self):
        return self.name


class Friendsgroup(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)


class Park(models.Model):
    """
    Park or similar Open Space.
    """

    ACCESS_CHOICES = (
        ('y', 'Yes'),
        ('n', 'No'),
        ('u', 'Unknown'),
    )

    os_id = models.CharField('OS ID', max_length=9, null=True, blank=True, help_text='Refers to MassGIS OS_ID')
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    alt_name = models.CharField('Alternative name', max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    neighborhoods = models.ManyToManyField(Neighborhood, related_name='neighborhoods')
    parktype = models.ForeignKey(Parktype, blank=True, null=True)
    parkowner = models.ForeignKey(Parkowner, blank=True, null=True)
    friendsgroup = models.ForeignKey("Friendsgroup", blank=True, null=True)
    events = models.ManyToManyField("Event", related_name="events", blank=True, null=True)
    access = models.CharField(max_length=1, blank=True, null=True, choices=ACCESS_CHOICES)
    area = models.FloatField()
    image = models.ImageField(blank=True, upload_to="parkimages")

    def parkimage_thumb(self):
         if self.image:
             thumb = default.backend.get_thumbnail(self.image.file, settings.ADMIN_THUMBS_SIZE)
             return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
         else:
             return None


    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Park')
        verbose_name_plural = _('Parks')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('park', [slugify(self.name)])

    def area_acres(self):
        return self.area / 4047

    def lat_long(self):
        self.geometry.transform(4326)
        return [self.geometry.centroid.y,self.geometry.centroid.x]

    def save(self, *args, **kwargs):

        self.area = self.geometry.area

        try:
            # cache containing neighorhood
            neighborhoods = Neighborhood.objects.filter(geometry__intersects=self.geometry)
            self.neighborhoods.clear()
            self.neighborhoods.add(*neighborhoods)
        except TypeError:
            self.neighborhoods = None

        if not self.slug:
            self.slug = slugify(self.name)

        while True:
            try:
                super(Park, self).save(*args, **kwargs)
            # slug fight
            except IntegrityError:
                transaction.rollback()
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
        super(Park, self).save(*args, **kwargs)


class Activity(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        super(Activity, self).save(*args, **kwargs)

    # FIXME: does code below require a unique slug field to work?
    #     while True:
    #         try:
    #             super(Activity, self).save()
    #         # Assuming the IntegrityError is due to a slug fight
    #         except IntegrityError:
    #             match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
    #             if match_obj:
    #                 next_int = int(match_obj.group(2)) + 1
    #                 self.slug = match_obj.group(1) + '-' + str(next_int)
    #             else:
    #                 self.slug += '-2'
    #         else:
    #             break


class Facilitytype(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(blank=False, upload_to="icons", null=False, help_text="Must be 32x37px to function properly")

    class Meta:
        verbose_name = _('Facilitytype')
        verbose_name_plural = _('Facilitytypes')

    def __unicode__(self):
        return self.name


class Facility(models.Model):
    """
    Facility in or outside a park.
    """

    name = models.CharField(max_length=50, blank=True, null=True)
    facilitytype = models.ForeignKey(Facilitytype, blank=True, null=True)
    activity = models.ManyToManyField(Activity, related_name='activity')
    location = models.CharField(max_length=50, blank=True, null=True, help_text='Address, nearby Landmark or similar location information.')
    status = models.CharField(max_length=50, blank=True, null=True)  # FIXME: choices?
    park = models.ForeignKey(Park, blank=True, null=True)
    notes = models.TextField(blank=True,)
    access = models.TextField(blank=True,)

    geometry = models.PointField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Facility')
        verbose_name_plural = _('Facilities')

    def parkimage_thumb(self):
         if self.park.image:
             thumb = default.backend.get_thumbnail(self.park.image.file, settings.ADMIN_THUMBS_SIZE)
             return u'<img width="%s" src="%s" />' % (thumb.width, thumb.url)
         else:
             return None

    def activity_string(self):
        out = []
        for activity in self.activity.all():
            out.append(activity.name)
        return ",".join(out)

    def parktype_string(self):
        return self.park.parktype

    def icon_url(self):
        if self.facilitytype.icon:
            return '%s' % (self.facilitytype.icon.url,)
        return '%sparkmap/img/icons/%s.png' % (settings.STATIC_URL, slugify(self.facilitytype))


    def admin_url(self):
        return reverse('admin:parkmap_facility_change', args=(self.id,))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            # cache containing park
            self.park = Park.objects.get(geometry__contains=self.geometry)
        except:
            self.park = None

        super(Facility, self).save(*args, **kwargs)

    # No page for facility exists yet. removing this
    #@models.permalink
    #def get_absolute_url(self):
    #    return ('facility', [slugify(self.name)])

class Story(models.Model):
    RATING_CHOICES = (
        ('1', "Happy"),
        ('2', "Blah"),
        ('3', "Idea"),
        ('4', "Sad"),
    )
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    rating = models.CharField(max_length=1, default='0', blank=False, null=False, choices=RATING_CHOICES)
    text = models.TextField(blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    park = models.ForeignKey(Park, blank=True, null=False)
    objectionable_content = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)
        
    @models.permalink
    def get_absolute_url(self):
        return ('parkmap.views.story', [str(self.id)])
