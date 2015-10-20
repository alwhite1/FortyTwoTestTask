from django.test import TestCase
from django.test.client import Client
from apps.requests.models import Requests
from apps.requests.tests.extra_function import send_request


class RequestsMiddlewareTest(TestCase):

    def test_request_middleware(self):
        """
        Check middleware for intercept request
        """
        send_request(5)
        count = Requests.objects.count()
        self.assertEqual(count, 5)

    def test_diff_type_of_request(self):
        """
        Check middleware for intercept get and post request.
        """
        client = Client()
        number_of_requests = Requests.objects.count()
        client.get("/requests/")
        self.assertEqual(number_of_requests + 1, Requests.objects.count())
        number_of_requests = Requests.objects.count()
        client.post("/requests/")
        self.assertEqual(number_of_requests + 1, Requests.objects.count())

    def test_for_ignoring_ajax_requests(self):
        """
        Check for ignoring ajax request.
        """
        number_of_requests = Requests.objects.count()
        client = Client()
        client.post("/requests/", **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(number_of_requests, Requests.objects.count())
