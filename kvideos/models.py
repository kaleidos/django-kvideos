# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import urllib


SERVICE_CHOICES = [
    ('youtube', 'You Tube'),
    ('vimeo', 'Vimeo'),
]

class Video(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    title = models.CharField(max_length=150, verbose_name=_(u'title'),
                             null=True, blank=True)
    description = models.TextField(verbose_name=_(u'description'), null=True,
                                   blank=True)
    typ = models.SlugField(max_length=25, choices=SERVICE_CHOICES,
                           verbose_name=_(u'type'), null=False, blank=False)
    code = models.CharField(max_length=100, verbose_name=_(u'code'),
                            null=False, blank=False)

    def clean(self):
        if self.typ == "youtube":
            validation_url = "http://gdata.youtube.com/feeds/api/videos/%s" % self.code
            conn = urllib.urlopen(validation_url)
            if conn.code != 200:
                raise ValidationError(_(u"%s id not found in YouTube" % self.code))
        elif self.typ == "vimeo":
            validation_url = "http://vimeo.com/api/v2/video/%s.json" % self.code 
            conn = urllib.urlopen(validation_url)
            if conn.code != 200:
                raise ValidationError(_(u"%s id not found in Vimeo" % self.code))
        else:
            raise ValidationError(_(u"%s is not a valid type of video." % self.typ))
