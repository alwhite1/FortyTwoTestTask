# -*- coding: utf-8 -*-
from django.shortcuts import render
from apps.person.models import Person
from apps.person.forms import EditPersonModelForm
from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.contrib.auth.views import login_required


def main(request):
    if Person.objects.count() > 0:
        person = Person.objects.last()
    else:
        person = {"name": "Name", "last_name": "Last name",
                  "date_of_birth": "Date of birth"}
    return render(request, 'main.html', {"person": person})


@login_required
def edit(request):
    if request.POST:
        if request.is_ajax():
            if Person.objects.count() > 0:
                form = EditPersonModelForm(request.POST, files=request.FILES, instance=Person.objects.last())
            else:
                form = EditPersonModelForm(request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponse('OK')
            else:
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)
                return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            return HttpResponse('Use ajax request')
    else:
        if Person.objects.count():
            form = EditPersonModelForm(instance=Person.objects.last())
        else:
            form = EditPersonModelForm()
        return render(request, 'edit.html', {'form': form})
    pass
