from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.db.utils import IntegrityError
from django.db import transaction
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from sorl.thumbnail import get_thumbnail, default

import re
import logging

logger = logging.getLogger(__name__)

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


class Parkimage(models.Model):
    """ Image taken in a park.
    """

    image = models.ImageField(upload_to='parkimages')
    caption = models.TextField(default='', blank=True)

    class Meta:
        verbose_name = _('Parkimage')
        verbose_name_plural = _('Parkimages')
        ordering = ['pk']

    def __unicode__(self):
        caption = getattr(self, 'caption', '')
        return '%i: %s' % (self.pk, strip_tags(caption))

    def thumbnail(self):
         if self.image:
             thumb = get_thumbnail(self.image.file, settings.ADMIN_THUMBS_SIZE, crop='center', quality=80)
             return u'<img width="%s" height="%s" src="%s" alt="%s" />' % (thumb.width, thumb.height, thumb.url, self.caption)
         else:
             return None
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True

    def get_parks_string(self):
        parks = [p.name for p in self.parks.all()]
        return ", ".join(parks)
    get_parks_string.short_description = 'Parks'
    

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
    neighborhoods = models.ManyToManyField(Neighborhood, related_name='neighborhoods', blank=True)
    parktype = models.ForeignKey(Parktype, blank=True, null=True)
    parkowner = models.ForeignKey(Parkowner, blank=True, null=True)
    friendsgroup = models.ForeignKey("Friendsgroup", blank=True, null=True)
    events = models.ManyToManyField("Event", related_name="events", blank=True, null=True)
    access = models.CharField(max_length=1, blank=True, null=True, choices=ACCESS_CHOICES)
    area = models.FloatField(blank=True, null=True)
    images = models.ManyToManyField(Parkimage, blank=True, null=True, related_name='parks')
    featured = models.BooleanField(default=False)

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Park')
        verbose_name_plural = _('Parks')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('park', ['%s-%d' % (slugify(self.name), self.id)])

    def area_acres(self):
        return self.area / 4047

    def lat_long(self):
        self.geometry.transform(4326)
        return [self.geometry.centroid.y,self.geometry.centroid.x]

    def get_image_thumbnails(self, include_large=False):
        # embed all images
        images = []
        tn_size = '250x250'
        large_size = '800x600'
        for i in self.images.all():
            try: 
                tn = get_thumbnail(i.image, tn_size, crop='center', quality=80)
                image = {
                    'src': tn.url,
                    'caption': strip_tags(i.caption),
                }
                if include_large:
                    try:
                        large_image = get_thumbnail(i.image, large_size, crop='center', quality=90)
                        image['large_src'] = large_image.url
                    except Exception, e:
                        logge.error(e)

                images.append(image)
            except IOError, e:
                logger.error(e)

        return images


    def to_external_document(self, user, include_large=False):
        change_url = None
        if user.has_perm('parks.change_park'):
            change_url = reverse('admin:parks_park_change', args=(self.id,))

        return {
            'url': self.get_absolute_url(),
            'name': self.name,
            'description': self.description,
            'images': self.get_image_thumbnails(include_large=include_large),
            'access': self.get_access_display(),
            'address': self.address,
            'owner': self.parkowner.name,
            'change_url': change_url
        }

    def save(self, *args, **kwargs):

        self.area = self.geometry.area
        # FIXME: we need a better slugify routine
        self.slug = '%s-%d' % (slugify(self.name), self.id)

        super(Park, self).save(*args, **kwargs)

        try:
            # cache containing neighorhood
            # doesn't work with admin forms, m2m get cleared during admin save
            # FIXME: improve routine - compare neighborhoods we intersect with against already stored neighborhoods
            neighborhoods = Neighborhood.objects.filter(geometry__intersects=self.geometry)
            self.neighborhoods.clear()
            self.neighborhoods.add(*neighborhoods)
        except TypeError:
            self.neighborhoods = None


class Activity(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        super(Activity, self).save(*args, **kwargs)


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
    facilitytype = models.ForeignKey(Facilitytype)
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

    def activity_string(self):
        out = []
        for activity in self.activity.all():
            out.append(activity.name)
        return ", ".join(out)
    activity_string.short_description = 'Activities'

    def parktype_string(self):
        return self.park.parktype

    def icon_url(self):
        if self.facilitytype.icon:
            return '%s' % (self.facilitytype.icon.url,)
        return '%sparks/img/icons/%s.png' % (settings.STATIC_URL, slugify(self.facilitytype))


    def admin_url(self):
        return reverse('admin:parks_facility_change', args=(self.id,))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            # cache containing park
            self.park = Park.objects.get(geometry__contains=self.geometry)
        except:
            self.park = None

        super(Facility, self).save(*args, **kwargs)


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
        return ('parks.views.story', [str(self.id)])

