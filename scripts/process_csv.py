import os
import pandas as pd
import time
from django.conf import settings
from api.models import Student, Course, Unit, Enrolment

# def read_csv():
#     rows = []
#     with open("scripts/dummy_data.csv", 'r') as file:
#         csvreader = csv.reader(file)
#         header = next(csvreader)
#         for row in csvreader:
#             rows.append(row)
#     print(header)
#     print(rows[-1])

# def run():
#     df = pd.read_csv('scripts/dummy_data.csv')
#     x = get_unique_student(df)
#     print(x)
#     a = [
#         [38866542, 'Michael Watson'],[41877053, 'Alison Ogden'], [41905875, 'Alan Hemmings'], [43199398, 'Owen Quinn'], [44678853, 'Jan Greene'], [44716329, 'Hannah Gibson'], [44883104, 'Blake Ferguson'], [45416518, 'Michael Miller'], [45416860, 'Cameron Berry'], [45629317, 'Alexander Morgan'], [45723445, 'Harry Ball'], [45789683, 'Richard Payne'], [45888033, 'Brandon Poole'], [46174698, 'Anna Bond'], [46224614, 'Charles Poole'], [46335201, 'Michael Stewart'], [46349895, 'Neil Arnold'], [46352732, 'Sam Kerr'], [46360595, 'Carl Rees'], [46360789, 'Natalie Walsh'], [46381783, 'Audrey Lee'], [46426312, 'Stewart Ferguson'], [46438074, 'Joseph Slater'], [46504890, 'Jacob Black'], [46547640, 'Joe Walker'], [46599109,
#     print(len(a))
#     print(len(x))

"""
TODO:
get unique student
find intake year + sem for commencement date (?) general studies and CS course are DIFFERENT.
has graduated default false? <- this is where process course credit points?
populate with above data

populate course (need faculty?)

populate unit (default name and code just put same or sth)

populate enrolment
NOTE:
general studies commencement date might be different! (Look at Dan Peake)
"""

course_to_faculty = dict()
FAILING_GRADES = [
    'N', 'DEF', 'NA', 'NGO', 'NA', 'NAS', 'E', 'NS', 'NH', 'NSR', 'WDN', 'WH', 'WI', 'WN'
]


def get_unique_student(df):
    student_identifier = [
        'PERSON ID', 'TITLE',
        'SURNAME', 'GIVEN NAMES', 'COMMENCEMENT_DT'
    ]
    df = df[student_identifier].drop_duplicates()
    df['NAME'] = df['SURNAME'] + ' ' + df['GIVEN NAMES']
    return list(map(tuple, df[['PERSON ID', 'NAME', 'COMMENCEMENT_DT']].values))


def get_unique_course(df):
    course_identifier = ['COURSE_CD', 'C_VER', 'CRS_TITLE']
    aux = df[course_identifier].drop_duplicates()
    return list(map(tuple, aux.values))


def register_enrolment(row):
    try:
        student = Student.objects.get(student_id=row['PERSON ID'])
        unit = Unit.objects.get(unit_code=row['UNIT_CD'])
        has_passed = False if row['GRADE'] in FAILING_GRADES else True
        enrolment, created = Enrolment.objects.update_or_create(
            student=student, unit=unit,
            enrolment_year=row['ACAD_YR'],
            enrolment_marks=row['MARK'],
            enrolment_grade=row['GRADE'],
            has_passed=has_passed
        )
    except Student.DoesNotExist:
        print(f"student id:{row['PERSON ID']} does not exist in the database")


def pc(file):
    start = time.time()
    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, file.upload.name))
    df.columns = df.columns.str.upper()
    df["COMMENCEMENT_DT"] = pd.to_datetime(df["COMMENCEMENT_DT"])
    print(f"Time taken to read file: {time.time() - start}")

    start = time.time()
    for code, version, title in get_unique_course(df):
        if not Course.objects.filter(course_code=code).exists():
            course, created = Course.objects.update_or_create(
                course_code=code, course_version=version,
                course_name=title, course_required_credits=144,
                course_curate_electives_credits=0
            )
    print(f"Time taken to process Courses: {time.time() - start}")

    start = time.time()
    for code in df["UNIT_CD"].unique():
        if not Unit.objects.filter(unit_code=code).exists():
            unit, created = Unit.objects.update_or_create(
                unit_code=code, unit_credits=6
            )
    print(f"Time taken to process Units: {time.time() - start}")

    start = time.time()
    for id, name, date in get_unique_student(df):
        if not Student.objects.filter(student_id=id).exists():
            student, created = Student.objects.update_or_create(
                student_id=id, student_name=name,
                student_intake_year=date.year,
                has_graduated=False
            )
    print(f"Time taken to process Students: {time.time() - start}")

    start = time.time()
    df.apply(func=register_enrolment, axis=1)
    print(f"Time taken to process Enrolments: {time.time() - start}")


def bulk_pc(file):
    start = time.time()
    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, file.upload.name))
    df.columns = df.columns.str.upper()
    df["COMMENCEMENT_DT"] = pd.to_datetime(df["COMMENCEMENT_DT"])
    print(f"Time taken to read file: {time.time() - start}")

    start = time.time()
    for code, version, title in get_unique_course(df):
        if not Course.objects.filter(course_code=code).exists():
            course, created = Course.objects.update_or_create(
                course_code=code, course_version=version,
                course_name=title, course_required_credits=144,
                course_curate_electives_credits=0
            )
    print(f"Time taken to process Courses: {time.time() - start}")

    start = time.time()
    for code in df["UNIT_CD"].unique():
        if not Unit.objects.filter(unit_code=code).exists():
            unit, created = Unit.objects.update_or_create(
                unit_code=code, unit_credits=6
            )
    print(f"Time taken to process Units: {time.time() - start}")

    start = time.time()
    for id, name, date in get_unique_student(df):
        if not Student.objects.filter(student_id=id).exists():
            student, created = Student.objects.update_or_create(
                student_id=id, student_name=name,
                student_intake_year=date.year,
                has_graduated=False
            )
    print(f"Time taken to process Students: {time.time() - start}")

    start = time.time()
    # process enrolments through bulk_create
    df_records = df.to_dict('records')

    enrolment_instances = [
        Enrolment(
            student=Student.objects.get(student_id=record['PERSON ID']),
            unit=Unit.objects.get(unit_code=record['UNIT_CD']),
            enrolment_year=record['ACAD_YR'],
            enrolment_marks=record['MARK'],
            enrolment_grade=record['GRADE'],
            has_passed=False if record['GRADE'] in FAILING_GRADES else True
        )
        for record in df_records
    ]

    Enrolment.objects.bulk_create(enrolment_instances)

    print(f"Time taken to process Enrolments: {time.time() - start}")
