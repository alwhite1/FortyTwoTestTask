from apps.requests.models import Requests


class InterceptRequests(object):

    def process_request(self, request):
        if not request.is_ajax():
            new_request = Requests(request=request)
            new_request.save()