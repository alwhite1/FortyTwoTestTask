from apps.requests.models import Requests


class InterceptRequests(object):

    def process_request(self, request):
        if not request.is_ajax():
            try:
                path=request.META['HTTP_HOST'] + request.META['PATH_INFO']
            except KeyError:
                path = "testserver"

            Requests(request=request, path=path).save()
