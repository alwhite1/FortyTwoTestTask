# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.person.views import main
from apps.person.models import Person
from django.core.urlresolvers import resolve
from django.test.client import Client


def check_db_content(contact, check_data):
    attributes = ("name", "last_name", "bio", "email", "jabber", "skype", "other_contacts")
    for attribute in attributes:
        if getattr(contact, attribute) != check_data[attribute]:
            print "contact: " + str(getattr(contact, attribute))
            print "dict: " + str(check_data[attribute])
            return False
    return True


def check_content_in_template(contact):
    attributes = ("name", "last_name", "email", "jabber", "skype", "other_contacts")
    client = Client()
    response = client.get("/")
    content = unicode(response.content, 'utf-8')
    for attribute in attributes:
        if not getattr(contact, attribute) in content:
            print getattr(contact, attribute)
            print content
            return False
    return True


def get_person_object(kind):
    object_array = (Person(name=u"new",
                           last_name=u"new",
                           date_of_birth="2001-02-02",
                           bio=u"new",
                           email=u"new@example.com",
                           jabber=u"new@example.com",
                           skype=u"new",
                           other_contacts=u"new"),
                    Person(name=u"Имя",
                           last_name=u"Фамилия",
                           date_of_birth="2001-02-02",
                           bio=u"Биография",
                           email=u"new@example.com",
                           jabber=u"new@example.com",
                           skype=u"new",
                           other_contacts=u"new"),
                    )
    if kind == "cyrillic":
        return object_array[1]
    elif kind == "simple":
        return object_array[0]


def get_check_data(kind):
    check_data_tuple = ({"name": u"name",
                         "last_name": u"last_name",
                         "date_of_birth": u"2000-01-01",
                         "bio": u"Bio.",
                         "email": u"test@example.com",
                         "jabber": u"test@example.com",
                         "skype": u"test",
                         "other_contacts": u"contacts"
                         },
                        {"name": u"new",
                         "last_name": u"new",
                         "date_of_birth": u"2001-02-02",
                         "bio": u"new",
                         "email": u"new@example.com",
                         "jabber": u"new@example.com",
                         "skype": u"new",
                         "other_contacts": u"new"
                         },
                        {"name": u"Имя",
                         "last_name": u"Фамилия",
                         "date_of_birth": "2001-02-02",
                         "bio": u"Биография",
                         "email": u"new@example.com",
                         "jabber": u"new@example.com",
                         "skype": u"new",
                         "other_contacts": u"new"
                         }
                        )
    if kind == "simple1":
        return check_data_tuple[0]
    elif kind == "simple2":
        return check_data_tuple[1]
    elif kind == "cyrillic":
        return check_data_tuple[2]


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
        check_data = get_check_data("simple1")
        self.assertEqual(check_db_content(contact, check_data), True)

    def test_add_new_person_and_delete(self):
        """
        Check can add and delete date from DB.
        """
        contact = get_person_object("simple")
        contact.save()
        contact = Person.objects.last()
        check_data = get_check_data("simple2")
        self.assertEqual(check_db_content(contact, check_data), True)
        Person.objects.last().delete()
        self.assertEqual(len(Person.objects.all()), 2)

    def test_cyrillic_support(self):
        """
        Check support DB for cyrillic language.
        """

        contact = get_person_object("cyrillic")
        check_data = get_check_data("cyrillic")
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(check_db_content(contact, check_data), True)

    def test_cyrillic_rendering(self):
        """
        Check rendering cyrillic to template
        """
        contact = get_person_object("cyrillic")
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact), True)


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
            contact = get_person_object("simple")
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
        contact = Person.objects.all()
        contact.delete()
        contact = get_person_object("simple")
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact), True)
        contact.name = "test_is_data_in_template_and_database_same"
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact), True)

class EditPersonModelFormTest(TestCase):

    fixtures = ['person/fixtures/test.json']

    def test_valid_data(self):

        form = EditPersonModelForm({
            'name': "John",
            'last_name': "Smith",
            'date_of_birth': '2000-01-01',
            'bio': "new bio",
            'email': "john_smith@example.com",
            'jabber': "john_smith@example.com",
            'skype': "john_smith",
            'other_contacts': "phone",
            'photo': "/bla/bla/bla.jpg"
        }, instance=Person.objects.get(id=1))
        self.assertTrue(form.is_valid())
        form.save()
        person = Person.objects.get(id=1)
        self.assertEqual(person.name, "John")
        self.assertEqual(person.last_name, "Smith")
        self.assertEqual(person.email, "john_smith@example.com")
        self.assertEqual(person.date_of_birth, datetime.date(2000, 1, 1))
        self.assertEqual(person.bio, "new bio")
        self.assertEqual(person.jabber, "john_smith@example.com")
        self.assertEqual(person.skype, "john_smith")
        self.assertEqual(person.other_contacts, "phone")
        self.assertEqual(person.photo, "/bla/bla/bla.jpg")