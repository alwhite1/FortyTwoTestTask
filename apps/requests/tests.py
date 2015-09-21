from django.test import TestCase
from django.core.urlresolvers import resolve
from apps.requests.views import requests
from requests.models import Requests
from django.test.client import Client


def send_request(number_of_request):
    client = Client()
    for i in xrange(0, int(number_of_request)):
        client.get('/')


class RequestsPageTest(TestCase):
    def test_url_resolves_to_request_page(self):
        found = resolve('/requests/')
        self.assertEqual(found.func, requests)

    def test_correct_requests_page_template(self):
        response = self.client.get('/requests/')
        self.assertTemplateUsed(response, 'requests.html')

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

    fixtures = ['apps/requests/fixtures/test_request.json']

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
    fixtures = ['apps/requests/fixtures/test_request.json', 'apps/person/fixtures/person.json']

    def test_request_middleware(self):
        send_request(5)
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
    fixtures = ['apps/requests/fixtures/test_request.json', 'apps/person/fixtures/person.json']

    def test_correct_response_for_request_quantity(self):
        start_request = int(self.client.post('/requests/').content)
        send_request(5)
        end_request = int(self.client.post('/requests/').content)
        self.assertEqual(end_request - start_request, 6)

    def test_correct_response_for_request_diff(self):
        start_request = int(self.client.post('/requests/').content)
        send_request(5)
        diff = int(self.client.post('/requests/', {'start_request': start_request},
                                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}).content)
        self.assertEqual(diff, 5)


