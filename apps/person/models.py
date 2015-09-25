# -*- coding: utf-8 -*-
from django.db import models
from PIL import Image, ImageOps
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from django.conf import settings

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
            if self.photo:
                person = Person.objects.last()
                old_photo = make_upload_path(person.photo.name.split('/')[len(person.photo.name.split("/")) - 1])
                os.remove(old_photo)
        if self.photo:
            img = Image.open(StringIO.StringIO(self.photo.read()))
            output = StringIO.StringIO()
            img = ImageOps.fit(img, (200, 200))
            img.save(output, format='JPEG', quality=99)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', self.photo.name, 'image/jpeg', output.len, None)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + " " + self.last_name
