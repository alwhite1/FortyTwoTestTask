from django.db import models


class Requests(models.Model):

    class Meta:
        db_table = 'Requests'

    path = models.CharField(max_length=64, default="")
    request = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.id)
