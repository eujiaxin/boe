from api.models import *
from django.db.utils import IntegrityError


def populate_school():
    f = Faculty.objects.create(
        faculty_name='School of Information Technology')
    c = Course.objects.create(
        course_code='C2001',
        course_name='Bachelor of Computer Science',
        faculty=f,
        course_required_credits=144,
        course_curate_electives_credits=12
    )
    s = Student.objects.create(
        student_id='30881676',
        course=c,
        student_name='Eu Jia Xin',
        student_email='jeuu0002@student.monash.edu',
        student_intake_year=2020,
        student_intake_semester='Semester 1',
        has_graduated=False
    )
    print(f)
    u = Unit.objects.create(
        unit_code='FIT1045',
        faculty=f,
        unit_name='Introduction to Algorithms',
        unit_credits=6
    )
    u2 = Unit.objects.create(
        unit_code='FIT1043',
        faculty=f,
        unit_name='Introduction to Data Science',
        unit_credits=6
    )


def run():
    populate_school()
