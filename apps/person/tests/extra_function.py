from django.test.client import Client


def check_db_content(contact, check_data):
    attributes = ("name", "last_name", "bio", "email", "jabber", "skype", "other_contacts")
    for attribute in attributes:
        if getattr(contact, attribute) != check_data[attribute]:
            print "contact: " + unicode(getattr(contact, attribute))
            print "dict: " + unicode(check_data[attribute])
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
