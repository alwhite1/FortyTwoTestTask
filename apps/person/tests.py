# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.person.views import main
from apps.person.models import Person
from django.core.urlresolvers import resolve
from django.test.client import Client
import datetime


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


class PersonModelTest(TestCase):

    fixtures = ['apps/person/fixtures/test.json']

    def test_for_existing_person(self):
        """
        Check DB for get info.
        """
        contact = Person.objects.last()
        self.assertEqual(contact.name, "name")
        self.assertEqual(contact.last_name, "last_name")
        self.assertEqual(contact.date_of_birth, datetime.date(2000, 1, 1))
        self.assertEqual(contact.bio, "Bio.")
        self.assertEqual(contact.email, "test@example.com")
        self.assertEqual(contact.jabber, "test@example.com")
        self.assertEqual(contact.skype, "test")
        self.assertEqual(contact.other_contacts, "contacts")

    def test_add_new_person_and_delete(self):
        """
        Check can add and delete date from DB.
        """
        contact = Person(name="new", last_name="new", date_of_birth="2001-02-02", bio="new", email="new", jabber="new", skype="new", other_contacts="new")
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(contact.name, "new")
        self.assertEqual(contact.last_name, "new")
        self.assertEqual(contact.date_of_birth, datetime.date(2001, 2, 2))
        self.assertEqual(contact.bio, "new")
        self.assertEqual(contact.email, "new")
        self.assertEqual(contact.jabber, "new")
        self.assertEqual(contact.skype, "new")
        self.assertEqual(contact.other_contacts, "new")
        Person.objects.last().delete()
        self.assertEqual(len(Person.objects.all()), 2)

    def test_cyrillic_support(self):
        """
        Check support DB for cyrillic language.
        """

        contact = Person(name="Имя", last_name="Фамилия", date_of_birth="2001-02-02",
                         bio="Биография", email="new", jabber="new",
                         skype="new", other_contacts="new")
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(contact.name, u"Имя")


class MainPageAdditionalTest(TestCase):

    def test_main_page_is_response_if_database_empty(self):
        """
        Check case what return to template if DB empty.
        """
        if Person.objects.count() > 0:
            contact = Person.objects.all()
            contact.delete()
            found = resolve('/')
        self.assertEqual(found.func, main)

    def test_main_page_if_in_database_more_that_one_record(self):
        """
        Check case what return in template if DB have  more that one record.
        """
        counter = 1
        while Person.objects.count() <= 1:
            contact = Person(name="new" + str(counter), last_name="new" + str(counter),
                             date_of_birth="2001-02-02", bio="new", email="new", jabber="new",
                             skype="new", other_contacts="new")
            contact.save()
            counter += 1
        contact_new = Person.objects.last()
        client = Client()
        response = client.get("/")
        self.assertContains(response, contact_new.name)

    def test_is_data_in_template_and_database_same(self):
        """
        Check that data in template and DB same.
        """
        contact = Person.objects.all()
        contact.delete()
        contact = Person(name="new", last_name="new", date_of_birth="2001-02-02",
                         bio="new", email="new", jabber="new", skype="new",
                         other_contacts="new")
        contact.save()
        contact = Person.objects.last()
        client = Client()
        response = client.get("/")
        self.assertContains(response, contact.name)
        contact.name = "test_is_data_in_template_and_database_same"
        contact.save()
        client = Client()
        response = client.get("/")
        self.assertContains(response, contact.name)
