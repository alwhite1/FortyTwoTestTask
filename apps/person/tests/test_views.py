# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test.client import Client
from django.test import TestCase
from apps.person.views import main
from apps.person.models import Person
from apps.person.factories import SimplePersonFactory, CyrillicPersonFactory
from apps.person.tests.extra_function import check_content_in_template


class MainPageTest(TestCase):

    def test_root_url_resolves_to_main_page(self):
        """
        Check for can resolve main page.
        """
        found = resolve('/')
        self.assertEqual(found.func, main)

    def test_correct_main_page_template(self):
        """
        See what template used for main page
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'main.html')

    def test_main_page_is_response_if_database_empty(self):
        """
        Check case is main page response if DB empty.
        """
        Person.objects.all().delete()
        client = Client()
        response = client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_main_page_context_if_database_empty(self):
        """
        Check case what return to template if DB empty.
        """
        Person.objects.all().delete()
        client = Client()
        response = client.get("/")
        person = response.context["person"]
        self.assertEquals(person['date_of_birth'], 'Date of birth')
        self.assertEquals(person['last_name'], 'Last name')
        self.assertEquals(person['name'], 'Name')

    def test_main_page_if_in_database_more_that_one_record(self):
        """
        Check case what return in template if DB have more that one record.
        """
        counter = 1
        while Person.objects.count() <= 1:
            contact = SimplePersonFactory.create()
            contact.name += str(counter)
            contact.last_name += str(counter)
            contact.save()
            counter += 1
        contact_new = Person.objects.last()
        self.assertEquals(check_content_in_template(contact_new), True)

    def test_is_data_in_template_and_database_same(self):
        """
        Check that data in template and DB same.
        """
        SimplePersonFactory.create()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact), True)
        contact.name = "test_is_data_in_template_and_database_same"
        contact.save()
        self.assertEqual(check_content_in_template(contact), True)

    def test_cyrillic_rendering(self):
        """
        Check rendering cyrillic to template
        """
        CyrillicPersonFactory.create()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact), True)
