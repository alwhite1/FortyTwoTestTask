from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from apps.requests.views import requests
from apps.requests.models import Requests
from apps.requests.tests.extra_function import send_request


class RequestsPageTest(TestCase):
    def test_url_resolves_to_request_page(self):
        """
        Check for can resolve requests page.
        """
        found = resolve('/requests/')
        self.assertEqual(found.func, requests)

    def test_correct_requests_page_template(self):
        """
        See what template used for requests page
        """
        response = self.client.get('/requests/')
        self.assertTemplateUsed(response, 'requests.html')

    def test_is_data_in_template_and_database_same(self):
        """
        Check that data in template and DB same.
        """
        if not Requests.objects.count():
            request = Requests(request="new_test")
            request.save()
        request = Requests.objects.last()
        client = Client()
        response = client.get("/requests/")
        self.assertContains(response, request.request)
        request.request = "test_is_data_in_template_and_database_same"
        request.save()
        client = Client()
        response = client.get("/requests/")
        self.assertContains(response, request.request)

    def test_correct_response_for_request_quantity(self):
        """
        Check that view return correct quantity of request.
        """
        start_request = int(self.client.post('/requests/').content)
        send_request(5)
        end_request = int(self.client.post('/requests/').content)
        self.assertEqual(end_request - start_request, 6)

    def test_correct_response_for_request_diff(self):
        """
        Check that view return correct diff between starting quantity of requests and current.
        """
        start_request = int(self.client.post('/requests/').content)
        send_request(5)
        diff = int(self.client.post('/requests/', {'start_request': start_request},
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}).content)
        self.assertEqual(diff, 5)
