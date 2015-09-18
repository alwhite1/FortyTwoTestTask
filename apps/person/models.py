from django.db import models


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

    def __unicode__(self):
        return self.name + " " + self.last_name
