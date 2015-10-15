from django.core.management.base import AppCommand


class Command(AppCommand):

    help = "Get all models that used at the projects"

    def handle(self, **options):
        return "I am command"
