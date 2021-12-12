from api.models import *


def run():
    models = [Student, Unit, Course, Faculty, Core,
              CuratedElective, Enrolment, CallistaDataFile]
    for model in models:
        model.objects.all().delete()
