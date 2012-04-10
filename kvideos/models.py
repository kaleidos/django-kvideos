from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

SERVICE_CHOICES = [
    ('youtube', 'You Tube'),
    ('vimeo', 'Vimeo'),
]

class Video(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    typ = models.SlugField(max_length=25, choices=SERVICE_CHOICES)
    code = models.CharField(max_length=100)
