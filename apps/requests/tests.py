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


class RequestsModelTest(TestCase):

    fixtures = ['apps/requests/fixtures/test_request.json']

    def test_for_existing_request(self):
        """
        Check DB for get info.
        """
        request = Requests.objects.last()
        self.assertEqual(request.request, "new")

    def test_add_new_request_and_delete(self):
        """
        Check can add and delete date from DB.
        """
        request = Requests(request="new_1")
        request.save()
        request = Requests.objects.get(id=2)
        self.assertEqual(request.request, "new_1")

        Requests.objects.get(id=2).delete()
        self.assertEqual(len(Requests.objects.all()), 1)


class RequestsMiddlewareTest(TestCase):
    fixtures = ['apps/requests/fixtures/test_request.json', 'apps/person/fixtures/person.json']

    def test_request_middleware(self):
        """
        Check middleware for intercept request
        """
        send_request(5)
        count = len(Requests.objects.all())
        self.assertEqual(count, 6)

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


class RequestFromAjax(TestCase):
    fixtures = ['apps/requests/fixtures/test_request.json', 'apps/person/fixtures/person.json']

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
