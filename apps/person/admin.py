from django.contrib import admin
from apps.person.models import Person, Signals


admin.site.register(Person)
admin.site.register(Signals)
