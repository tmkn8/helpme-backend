from decimal import Decimal
import math

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


DEFAULT_RADIUS_MILES = getattr(settings, 'HELPME_DEFAULT_RADIUS_MILES',
                               float(1))
EQUATORIAL_CIRCUMFERENCE = 24901
POLAR_CIRCUMFERENCE = 24860
ONE_MILE_LATITUDE_DEGREES = float(360) / float(EQUATORIAL_CIRCUMFERENCE)
ONE_MILE_LONGITUDE_DEGREES = float(360) / float(POLAR_CIRCUMFERENCE)


class HelpRequestQuerySet(models.query.QuerySet):
    def location(self, latitude, longitude, radius=DEFAULT_RADIUS_MILES):
        """
        This method takes latitude, longitude and radius in miles as
        parameters and shows help requests which are in the given radius.
        """
        # Convert values to floating point type
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)

        # Calculate boundaries of supplied coordinates according to radius
        # supplied in miles
        max_val = {
            'north': latitude + (ONE_MILE_LATITUDE_DEGREES * radius),
            'south': latitude - (ONE_MILE_LATITUDE_DEGREES * radius),
            'east': longitude + (ONE_MILE_LONGITUDE_DEGREES * radius),
            'west': longitude - (ONE_MILE_LONGITUDE_DEGREES * radius)
        }

        return self.filter(
            location_lat__range=(max_val['south'], max_val['north']),
            location_lon__range=(max_val['west'], max_val['east'])
        )


class HelpRequestManager(models.Manager):
    def get_queryset(self):
        return HelpRequestQuerySet(self.model, using=self._db)

    def location(self, latitude, longitude, radius=DEFAULT_RADIUS_MILES):
        return self.get_queryset().location(latitude, longitude, radius)


class HelpRequest(models.Model):
    title = models.CharField(_('title'), max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'))
    datetime = models.DateTimeField(_('datetime'), default=timezone.now)
    location_name = models.CharField(_('meeting location name'), max_length=50)
    location_lat = models.FloatField(_('meeting location latitude'), blank=True, null=True)
    location_lon = models.FloatField(_('meeting location longitude'), blank=True, null=True)
    content = models.TextField(_('content'))
    is_closed = models.BooleanField(_('is closed'), default=False)
    objects = HelpRequestManager()

    class Meta:
        verbose_name = _('help request')
        verbose_name_plural = _('help requests')

    def __str__(self):
        return self.title

    @property
    def author_name(self):
        return self.author.get_full_name()

    def get_distance(self, user_longitude, user_latitude):
        # Convert given coordinated to floating point
        user_longitude = float(user_longitude)
        user_latitude = float(user_latitude)

        # Use the formula for distance between two points
        x = math.pow(user_longitude - self.longitude, 2)
        y = math.pow(user_latitude - self.latitude, 2)
        return math.sqrt(x + y)
