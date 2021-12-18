import os
import time

from api.models import Student, Course, Unit, Enrolment
from django.shortcuts import get_object_or_404


def validate_graduation(students):
    res = dict()
    for id, _, _, course_code, course_version in students:
        course = get_object_or_404(
            Course,
            course_code=course_code,
            course_version=course_version
        )
        student = get_object_or_404(
            Student,
            student_id=id,
            course=course
        )
        enrolments = set([
            e.unit.unit_code for e in student.enrolment_set.all() if e.has_passed
        ])
        cores = set([
            c.unit.unit_code for c in course.core_set.all()
        ])
        missing_cores = cores.difference(enrolments)
        if len(missing_cores) <= 0:
            student.has_graduated = True
            student.save()
        # res[id] = (student.has_graduated, str(missing_cores))
        res[student] = (course, missing_cores)
    return res
