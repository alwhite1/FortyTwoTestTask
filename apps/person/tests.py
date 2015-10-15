# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.person.views import main
from apps.person.models import Person
from apps.person.forms import EditPersonModelForm
from django.core.urlresolvers import resolve
from django.test.client import Client
import StringIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from apps.person.templatetags.edit_link import edit_link


def check_db_content(contact, check_data):
    attributes = ("name", "last_name", "bio", "email", "jabber", "skype", "other_contacts")
    for attribute in attributes:
        if getattr(contact, attribute) != check_data[attribute]:
            return False
    return True


def check_content_in_template(contact, link):
    attributes = ("name", "last_name", "email", "jabber", "skype", "other_contacts")
    client = Client()
    if link == "/edit/":
        client.login(username="test", password="test")
    response = client.get(link)
    content = unicode(response.content, 'utf-8')
    for attribute in attributes:
        if not getattr(contact, attribute) in content:
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
                         },
                        {
                        'name': "John",
                        'last_name': "Smith",
                        'date_of_birth': '2000-01-01',
                        'bio': "new bio",
                        'email': "john_smith@example.com",
                        'jabber': "john_smith@example.com",
                        'skype': "john_smith",
                        'other_contacts': "phone",
                        'photo': 'test.jpg'
                        },
                        {
                        "name": u"Имя",
                        "last_name": u"Фамилия",
                        "date_of_birth": "2001-02-02",
                        "bio": u"Биография",
                        "email": u"new@example.com",
                        "jabber": u"new@example.com",
                        "skype": u"new",
                        "other_contacts": u"new",
                        'photo': 'тест.jpg'
                        }
                        )
    if kind == "simple1":
        return check_data_tuple[0]
    elif kind == "simple2":
        return check_data_tuple[1]
    elif kind == "cyrillic":
        return check_data_tuple[2]
    elif kind == "form":
        return check_data_tuple[3]
    elif kind == "form_cyrillic":
        return check_data_tuple[4]


def get_temp_photo(photo_name):
    io = StringIO.StringIO()
    size = (300, 300)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='JPEG')
    image_file = InMemoryUploadedFile(io, None, photo_name, 'jpeg', io.len, None)
    image_file.seek(0)
    return image_file


def clear_db():
    if Person.objects.count() > 0:
        contact = Person.objects.all()
        contact.delete()
    pass


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
        self.assertEqual(check_content_in_template(contact, "/"), True)


class MainPageAdditionalTest(TestCase):

    def test_main_page_is_response_if_database_empty(self):
        """
        Check case what return to template if DB empty.
        """
        clear_db()
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
        self.assertEquals(check_content_in_template(contact_new, "/"), True)

    def test_is_data_in_template_and_database_same(self):
        """
        Check that data in template and DB same.
        """
        contact = Person.objects.all()
        contact.delete()
        contact = get_person_object("simple")
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact, "/"), True)
        contact.name = "test_is_data_in_template_and_database_same"
        contact.save()
        contact = Person.objects.last()
        self.assertEqual(check_content_in_template(contact, "/"), True)


class EditPersonModelFormTest(TestCase):

    fixtures = ['apps/person/fixtures/test.json']

    def test_valid_data(self):
        """
        Check form for correct work.
        """
        photo_file = get_temp_photo('test.jpg')
        form = EditPersonModelForm(get_check_data("form"), {"photo": photo_file})
        self.assertTrue(form.is_valid())

    def test_data_in_cyrillic(self):
        """
        Check form for correct work with cyrillic data.
        """
        photo_file = get_temp_photo('тест.jpg')
        form = EditPersonModelForm(get_check_data("form_cyrillic"), {"photo": photo_file})
        self.assertTrue(form.is_valid())


class EditPageTest(TestCase):

    def test_form_return_all_field_to_template(self):
        """
        Check that all form field represent in edit page
        """
        pass


class EditPersonViewTest(TestCase):

    fixtures = ['apps/person/fixtures/test.json']

    def setUp(self):
        self.client = Client()
        self.username = 'test'
        self.email = 'test@example.com'
        self.password = 'test'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def test_login_require(self):
        """
        Check that edit page require login
        """
        response = self.client.get('/edit')
        self.assertEqual(response.status_code, 301)
        self.assertTrue(isinstance(response, HttpResponsePermanentRedirect))
        self.assertEqual(response.url, 'http://testserver/edit/')
        self.assertTemplateNotUsed(response, 'edit.html')

    def test_login_availability(self):
        """
        Check that can login.
        """
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)
        login = self.client.login(username="fake_user", password="fake_password")
        self.assertEqual(login, False)

    def test_get_request_when_database_is_empty(self):
        """
        Check what received if send get request when database is empty
        """
        self.client.login(username=self.username, password=self.password)
        attributes = ("name", "last_name", "bio", "email", "jabber", "skype", "other_contacts")
        clear_db()
        response = self.client.get('/edit/')
        for item in attributes:
            try:
                if response.context[item]:
                    check = False
            except KeyError:
                check = True
        self.assertEqual(check, True)

    def test_get_request_when_database_not_empty(self):
        """
        Check what received if send get request when database not empty
        """

        contact = get_person_object("simple")
        contact.save()
        self.assertEqual(check_content_in_template(contact, "/edit/"), True)

    def test_ajax_request_if_database_empty(self):
        """
        Check what received if send post request when database is empty
        """
        clear_db()
        self.client.login(username=self.username, password=self.password)
        form = get_check_data("form")
        form["photo"] = get_temp_photo('test.jpg')
        self.client.post("/edit/", form, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        contact = Person.objects.last()
        self.assertEqual(check_db_content(contact, get_check_data("form")), True)

    def test_ajax_request_if_database_not_empty(self):
        """
        Check what received if send post request when database not empty
        """
        clear_db()
        contact = get_person_object("simple")
        contact.save()
        self.client.login(username=self.username, password=self.password)
        form = get_check_data("form")
        form["photo"] = get_temp_photo('test.jpg')
        self.client.post("/edit/", form, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        contact = Person.objects.last()
        self.assertEqual(check_db_content(contact, get_check_data("form")), True)

    def test_post_request_not_ajax(self):
        """
        Check what received if send not ajax request
        """
        self.client.login(username=self.username, password=self.password)
        form = get_check_data("form")
        response = self.client.post("/edit/", form)
        self.assertEqual(response.content, "Use ajax request")

    def test_post_request_error_message(self):
        """
        Check what happens if send correct data in form
        """
        self.client.login(username=self.username, password=self.password)
        form = get_check_data("form")
        response = self.client.post("/edit/", form, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn("photo", response.content)
        self.assertIn("This field is required", response.content)

    def test_post_request_with_not_valid_data(self):
        """
        Check what happens if send invalid data in form
        """
        pass


class CustomTagTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'test'
        self.email = 'test@example.com'
        self.password = 'test'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def test_tag_return_expected_url(self):
        """
        Check that tag return expected url for a given object
        """
        contact = Person.objects.last()
        url = edit_link(contact)
        self.assertEqual(url, "/admin/person/person/1/")

    def test_tag_return_exist_url(self):
        """
        Check that url page is response.
        """
        contact = Person.objects.last()
        url = edit_link(contact)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tag_return_if_db_is_empty(self):
        """
        Check what return tag if DB is empty.
        """
        clear_db()
        url = edit_link()
        self.assertEqual(url, "/admin/")
