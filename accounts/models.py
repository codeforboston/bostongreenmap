from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    first_name = models.CharField(max_length=100, blank=True, null=False,
                                  default='')
    last_name = models.CharField(max_length=100, blank=True, null=False,
                                 default='')
    favorite_park = models.ForeignKey('parks.Park', null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail',
                (),
                dict(username=self.user.username))

    def display_name(self):
        hname = ' '.join([n for n in (self.first_name, self.last_name)
                          if n])
        if not hname:
            return self.user.username
        return '%s (%s)' % (hname, self.user.username)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
