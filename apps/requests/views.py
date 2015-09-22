from django.shortcuts import render
from apps.requests.models import Requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def requests(request):
    quantity_of_request = len(Requests.objects.all())
    if request.method == 'POST':
        if request.is_ajax():
            start_request = request.POST.get('start_request', None)
            if start_request is None:
                start_request = 0
            diff = quantity_of_request - int(start_request)
            return HttpResponse(diff)
        return HttpResponse(quantity_of_request)
    if len(Requests.objects.all()) > 10:
        last_10_requests = Requests.objects.all()[len(Requests.objects.all()) - 10:]
        quantity_of_request = len(Requests.objects.all())
        return render(request, 'requests.html', {'requests': last_10_requests,
                                                 'quantity_of_request': quantity_of_request})
    last_10_requests = Requests.objects.all()
    quantity_of_request = len(Requests.objects.all())
    return render(request, 'requests.html', {'requests': last_10_requests,
                                             'quantity_of_request': quantity_of_request})
