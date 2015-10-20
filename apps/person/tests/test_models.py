# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.person.models import Person
from apps.person.factories import SimplePersonFactory, CyrillicPersonFactory
from apps.person.tests.extra_function import check_db_content, check_content_in_template


class PersonModelTest(TestCase):

    def test_for_existing_person(self):
        """
        Check DB for get info.
        """
        contact = SimplePersonFactory.create()
        check_data = SimplePersonFactory.attributes()
        self.assertEqual(check_db_content(contact, check_data), True)

    def test_add_new_person_and_delete(self):
        """
        Check can add and delete date from DB.
        """
        Person.objects.all().delete()
        contact = SimplePersonFactory.create()
        check_data = SimplePersonFactory.attributes()
        self.assertEqual(check_db_content(contact, check_data), True)
        Person.objects.last().delete()
        self.assertEqual(Person.objects.count(), 0)

    def test_cyrillic_support(self):
        """
        Check support DB for cyrillic language.

        """
        Person.objects.all().delete()
        contact = CyrillicPersonFactory.create()
        check_data = CyrillicPersonFactory.attributes()
        self.assertEqual(check_db_content(contact, check_data), True)

    def test_cyrillic_rendering(self):
        """
        Check rendering cyrillic to template
        """
        CyrillicPersonFactory.create()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact), True)
