from django.shortcuts import render
from apps.person.models import Person


def main(request):
    if Person.objects.count() > 0:
        person = Person.objects.last()
    else:
        person = {"name": "Name", "last_name": "Last name",
                  "date_of_birth": "Date of birth"}
    return render(request, 'main.html', {"person": person})
