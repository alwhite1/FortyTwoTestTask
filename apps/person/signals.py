from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.person.models import Person, Signals
from apps.requests.models import Requests


@receiver(post_save, sender=Person)
@receiver(post_save, sender=Requests)
def object_saved(sender, **kwargs):
    Signals(model=str(sender).split(" ")[1].split("'")[1].split(".")[-1], action='Saved: {}'.format(kwargs['instance'].__dict__)).save()


@receiver(post_delete, sender=Person)
@receiver(post_delete, sender=Requests)
def object_delete(sender, **kwargs):
    Signals(model=str(sender).split(" ")[1].split("'")[1].split(".")[-1], action='Delete: {}'.format(kwargs['instance'].__dict__)).save()
