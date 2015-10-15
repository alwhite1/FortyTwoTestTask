from django.core.management.base import BaseCommand
from django.db.models import get_models, get_app
from django.conf import settings


class Command(BaseCommand):

    help = "Get all models that used at the projects"

    def handle(self, **options):
        model_list = ["model:objects"]
        all_app = settings.INSTALLED_APPS
        for app in all_app:
            if app != "django_coverage":
                app = app.split(".")[-1]
                for model in get_models(get_app(app)):
                    info = str(model.__name__) + ":" + str(model._default_manager.count())
                    model_list.append(info)
        return "\n".join(model_list)
