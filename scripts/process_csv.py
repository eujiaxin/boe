import os
import pandas as pd
import time
from django.conf import settings
from api.models import Student, Course, Unit, Enrolment
from scripts.process_reqs import validate_graduation

"""
TODO:
get unique student
find intake year + sem for commencement date (?) general studies and CS course are DIFFERENT.
has graduated default false? <- this is where process course credit points?
populate with above data

populate course (need faculty?)

NOTE:
general studies commencement date might be different! (Look at Dan Peake)
"""

course_to_faculty = dict()
FAILING_GRADES = [
    'N', 'DEF', 'NA', 'NGO', 'NA', 'NAS', 'E', 'NS', 'NH', 'NSR', 'WDN', 'WH', 'WI', 'WN'
]
unique_students = []


def get_unique_student(df):
    student_identifier = [
        'PERSON ID', 'TITLE',
        'SURNAME', 'GIVEN NAMES', 'COMMENCEMENT_DT', 'COURSE_CD', 'C_VER'
    ]
    df = df[student_identifier].drop_duplicates()
    df['NAME'] = df['SURNAME'] + ' ' + df['GIVEN NAMES']
    return list(map(tuple, df[['PERSON ID', 'NAME', 'COMMENCEMENT_DT', 'COURSE_CD', 'C_VER']].values))


def get_unique_course(df):
    course_identifier = ['COURSE_CD', 'C_VER', 'CRS_TITLE']
    aux = df[course_identifier].drop_duplicates()
    return list(map(tuple, aux.values))


def process_courses(df):
    for code, version, title in get_unique_course(df):
        if not Course.objects.filter(course_code=code, course_version=version).exists():
            course, created = Course.objects.update_or_create(
                course_code=code, course_version=version,
                course_name=title, course_required_credits=144,
                course_curate_electives_credits=0
            )


def process_units(df):
    for code in df["UNIT_CD"].unique():
        if not Unit.objects.filter(unit_code=code).exists():
            unit, created = Unit.objects.update_or_create(
                unit_code=code, unit_credits=6
            )


def process_students(df):
    global unique_students
    unique_students = get_unique_student(df)
    for id, name, date, course_code, course_version in unique_students:
        course = Course.objects.get(
            course_code=course_code,
            course_version=course_version
        )
        if not Student.objects.filter(student_id=id, course=course).exists():
            student, created = Student.objects.update_or_create(
                student_id=id, student_name=name,
                course=course,
                student_intake_year=date.year,
                has_graduated=False
            )


def process_enrolments(df):
    important_fields = ['PERSON ID', 'UNIT_CD',
                        'ACAD_YR', 'MARK', 'GRADE', 'CAL_TYPE', 'COURSE_CD', 'C_VER']
    df_records = df[important_fields].drop_duplicates().to_dict('records')
    enrolment_instances = []
    for record in df_records:
        course = Course.objects.get(
            course_code=record['COURSE_CD'],
            course_version=record['C_VER'],
        )
        student = Student.objects.get(
            student_id=record['PERSON ID'],
            course=course
        )
        enrolment_instances.append(
            Enrolment(
                student=student,
                unit=Unit.objects.get(unit_code=record['UNIT_CD']),
                enrolment_year=record['ACAD_YR'],
                enrolment_semester=record['CAL_TYPE'],
                enrolment_marks=record['MARK'],
                enrolment_grade=record['GRADE'],
                has_passed=False if record['GRADE'] in FAILING_GRADES else True
            )
        )
    Enrolment.objects.bulk_create(enrolment_instances, ignore_conflicts=True)


def bulk_pc(file, alt=False):
    global unique_students
    start = time.time()
    if alt:
        df = pd.read_csv(file)
    else:
        df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, file.upload.name))
    df.columns = df.columns.str.upper()
    df["COMMENCEMENT_DT"] = pd.to_datetime(df["COMMENCEMENT_DT"])
    print(f"Time taken to read file: {time.time() - start}")

    start = time.time()
    process_courses(df)
    print(f"Time taken to process Courses: {time.time() - start}")

    start = time.time()
    process_units(df)
    print(f"Time taken to process Units: {time.time() - start}")

    start = time.time()
    process_students(df)
    print(f"Time taken to process Students: {time.time() - start}")

    start = time.time()
    process_enrolments(df)
    print(f"Time taken to process Enrolments: {time.time() - start}")

    student_objects = []
    for id, _, _, course_code, course_version in unique_students:
        s = Student.objects.get(student_id=id, course=Course.objects.get(
            course_code=course_code, course_version=course_version))
        student_objects.append(s)

    return student_objects
