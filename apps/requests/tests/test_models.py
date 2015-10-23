from django.test import TestCase
from apps.requests.models import Requests


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
        request = Requests(request="new_1", path="new")
        request.save()
        request = Requests.objects.get(id=2)
        self.assertEqual(request.request, "new_1")
        self.assertEqual(request.path, "new")
        Requests.objects.get(id=2).delete()
        self.assertEqual(Requests.objects.count(), 1)
