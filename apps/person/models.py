# -*- coding: utf-8 -*-
from django.db import models
from PIL import Image, ImageOps
from django.conf import settings
import os


def make_upload_path(filename):
        return u"".join(os.path.split(settings.BASE_DIR)[:len(os.path.split(settings.BASE_DIR)) - 1]) +\
               u'/uploads/images/%s' % filename


class Person(models.Model):

    def Meta():
        db_table = 'person'

    name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.CharField(max_length=32)
    skype = models.CharField(max_length=32)
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to='images/', blank=True)

    def save(self, *args, **kwargs):
        if self.photo:
            filename = make_upload_path(self.photo.name)
            img = Image.open(filename)
            img = ImageOps.fit(img, (200, 200))
            img.save(self.photo)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + " " + self.last_name
