from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.requests.models import Requests


@ensure_csrf_cookie
def requests(request):
    quantity_of_request = Requests.objects.count()
    if request.method == 'POST':
        if request.is_ajax():
            start_request = request.POST.get('start_request', None)
            if start_request is None:
                start_request = 0
            diff = quantity_of_request - int(start_request)
            return HttpResponse(diff)
        return HttpResponse(quantity_of_request)
    if quantity_of_request > 10:
        last_10_requests = Requests.objects.all()[quantity_of_request - 10:]
        return render(request, 'requests_new.html', {'requests': last_10_requests,
                                                     'quantity_of_request': quantity_of_request})
    last_10_requests = Requests.objects.all()
    return render(request, 'requests_new.html', {'requests': last_10_requests,
                                                 'quantity_of_request': quantity_of_request})
