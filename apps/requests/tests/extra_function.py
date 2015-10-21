from django.test.client import Client


def send_request(number_of_request):
    client = Client()
    for i in xrange(0, int(number_of_request)):
        client.get('/')
