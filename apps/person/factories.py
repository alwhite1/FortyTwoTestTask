# -*- coding: utf-8 -*-
import factory
from apps.person.models import Person


class SimplePersonFactory(factory.Factory):

    FACTORY_FOR = Person

    name = u"new"
    last_name = u"new"
    date_of_birth = "2001-02-02"
    bio = u"new"
    email = u"new@example.com"
    jabber = u"new@example.com"
    skype = u"new"
    other_contacts = u"new"


class CyrillicPersonFactory(factory.Factory):

    FACTORY_FOR = Person

    name = u"Имя"
    last_name = u"Фамилия"
    date_of_birth = "2001-02-02"
    bio = u"new"
    email = u"new@example.com"
    jabber = u"new@example.com"
    skype = u"new"
    other_contacts = u"new"
