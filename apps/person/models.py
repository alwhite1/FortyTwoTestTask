# -*- coding: utf-8 -*-
from django.db import models
from PIL import Image, ImageOps
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


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
            img = Image.open(StringIO.StringIO(self.photo.read()))
            output = StringIO.StringIO()
            img = ImageOps.fit(img, (200, 200))
            img.save(output, format='JPEG', quality=99)
            output.seek(0)
            self.photo = InMemoryUploadedFile(output, 'ImageField', self.photo.name, 'image/jpeg', output.len, None)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + " " + self.last_name
