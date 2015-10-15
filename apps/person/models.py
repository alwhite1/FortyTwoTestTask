# -*- coding: utf-8 -*-
from django.db import models
from PIL import Image, ImageOps
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from django.conf import settings


def cut_image(photo):
    img = Image.open(StringIO.StringIO(photo.read()))
    output = StringIO.StringIO()
    img = ImageOps.fit(img, (200, 200))
    img.save(output, format='JPEG', quality=99)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', photo.name, 'image/jpeg', output.len, None)


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
        if Person.objects.count() > 0:

            if self.photo.name != Person.objects.last().photo.name:
                old_photo_name = Person.objects.last().photo.name.split('/')[-1]
                if old_photo_name:
                    os.remove(make_upload_path(old_photo_name))
                self.photo = cut_image(self.photo)

        elif Person.objects.count() == 0:
            if self.photo:
                self.photo = cut_image(self.photo)

        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + " " + self.last_name
