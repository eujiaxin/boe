import pandas as pd
from api.models import Student, Course, Unit, Enrolment

df = pd.read_csv("dummy_data.csv")

course_req = df.groupby(["COURSE_CD", "C_VER"])["UNIT_CD"]\
    .apply(list)\
    .reset_index(name='new').to_dict("records")

for record in course_req:
    course = Course.objects.filter(
        course_code=record["COURSE_CD"], course_version=record["C_VER"]
    )[0]
