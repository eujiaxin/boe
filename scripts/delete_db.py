from api.models import *


def run():
    models = [Student, Unit, Course, Faculty]
    for model in models:
        model.objects.all().delete()
