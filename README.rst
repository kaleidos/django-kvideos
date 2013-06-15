Django Kaleidos Videos
======================

.. image:: https://travis-ci.org/kaleidos/django-kvideos.png?branch=master
    :target: https://travis-ci.org/kaleidos/django-kvideos

.. image:: https://coveralls.io/repos/kaleidos/django-kvideos/badge.png?branch=master
    :target: https://coveralls.io/r/kaleidos/django-kvideos?branch=master

.. image:: https://pypip.in/v/django-kvideos/badge.png
    :target: https://crate.io/packages/django-kvideos

.. image:: https://pypip.in/d/django-kvideos/badge.png
    :target: https://crate.io/packages/django-kvideos

Django Kaleidos Videos is a django application for add videos (from services
like youtube or vimeo) to any model.

Suported video services
-----------------------

* Youtube
* Vimeo

Configuration
-------------

Configure the app in your setting INSTALLED_APPS::

  INSTALLED_APPS = [
     ...
     kvideos,
     ...
  ]

Configure, if you want, the default video size in your settings.py::

  KVIDEOS_DEFAULT_SIZE = "640x480"

For easy access to the videos, add to your models a generic relation to kvideos.models.Video model, for example::

  from kvideos.models import Video
  from django.contrib.contenttypes.generic import GenericRelation

  class MyModel(models.Model):
      ... # my fields
      videos = GenericRelation(Video)

For integrate it with the admin panel, you can add a new inline to your models admin classes, for example::

  from django.contrib.contenttypes.generic import GenericTabularInline
  from kvideos.models import Video
  
  class VideoInline(GenericTabularInline):
      model = Video
  
  class MyModelAdmin(admin.ModelAdmin):
      model = models.MyModel
      inlines = [MyOtherInlines, ...,  VideoInline]

Usage
-----

Now you can add videos to any of your models, and can show this on your web page througth the embed_video template tag, for example::

  <div>
    {% for video in myobject.videos.all %}
      {% if forloop.first %}
        {{ video.title }}
        {% embed_video video 800x600 %} <!-- Big video first -->
        {{ video.description }}
      {% else %}
        {{ video.title }}
        {% embed_video video %} <!-- Default size videos -->
      {% endif %}
    {% endfor %}
  </div>
