from django.test import TestCase
from django.core.urlresolvers import resolve
from requests.views import requests_page
from requests.models import Requests
from django.test.client import Client


class RequestsPageTest(TestCase):
    def test_url_resolves_to_request_page(self):
        found = resolve('/requests/')
        self.assertEqual(found.func, requests_page)

    def test_correct_requests_page_template(self):
        response = self.client.get('/requests/')
        self.assertTemplateUsed(response, 'requests_page.html')

    def test_is_data_in_template_and_database_same(self):
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

class RequestsModelTest(TestCase):

    fixtures = ['requests/fixtures/test_request.json']

    def test_for_existing_request(self):
        requests = Requests.objects.get(id=1)
        self.assertEqual(requests.request, "new")

    def test_add_new_request_and_delete(self):
        requests = Requests(request="new_1")
        requests.save()
        requests = Requests.objects.get(id=2)
        self.assertEqual(requests.request, "new_1")

        Requests.objects.get(id=2).delete()
        self.assertEqual(len(Requests.objects.all()), 1)

class RequestsMiddlewareTest(TestCase):
    fixtures = ['requests/fixtures/test_request.json', 'person/fixtures/person.json']

    def test_request_middleware(self):
        for i in xrange(0, 5):
            self.client.get('/')
        count = len(Requests.objects.all())
        self.assertEqual(count, 6)

    def test_diff_type_of_request(self):
        client = Client()
        response = client.get("/requests/")
        self.assertContains(response, "GET")
        response = client.post("/requests/")
        response = client.get("/requests/")
        self.assertContains(response, "POST")

class RequestFromAjax(TestCase):
    fixtures = ['requests/fixtures/test_request.json', 'person/fixtures/person.json']

    def test_correct_response_for_request_quantity(self):
        start_request = int(self.client.post('/requests/').getvalue())
        for i in xrange(0, 5):
            self.client.get('/')
        end_request = int(self.client.post('/requests/').getvalue())
        self.assertEqual(end_request - start_request, 6)
