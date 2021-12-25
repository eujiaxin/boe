from api.models import *
from django.db.utils import OperationalError


def run():
    models = [Student, Unit, Course, Faculty, Core, CoreList,
              CuratedElective, Enrolment, CallistaDataFile]
    for model in models:
        try:
            model.objects.all().delete()
        except OperationalError:
            print(f"table {model} not found")
