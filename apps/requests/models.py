from django.db import models


class Requests(models.Model):

    class Meta:
        db_table = 'Requests'

    request = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.date
