import os
import pandas as pd
from api.models import Course, Unit, Core
from django.shortcuts import get_object_or_404
from django.conf import settings


def run():
    script_path = os.path.join(settings.BASE_DIR, "scripts")
    df = pd.read_csv(os.path.join(script_path, "dummy_data.csv"))

    course_req = df.groupby(["COURSE_CD", "C_VER"])["UNIT_CD"]\
        .apply(list)\
        .reset_index(name='UNITS').to_dict("records")

    for record in course_req:
        course = get_object_or_404(
            Course,
            course_code=record["COURSE_CD"], course_version=record["C_VER"]
        )
        for unit_code in record["UNITS"]:
            unit = get_object_or_404(
                Unit,
                unit_code=unit_code
            )
            Core.objects.update_or_create(
                course=course, unit=unit
            )
