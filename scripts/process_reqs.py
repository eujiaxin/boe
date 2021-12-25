import os
import time

from api.models import Student, Course, Unit, Enrolment
from django.shortcuts import get_object_or_404


def validate_graduation(students):
    res = dict()
    for student in students:
        course = get_object_or_404(
            Course,
            course_code=student.course.course_code,
            course_version=student.course.course_version
        )
        student = get_object_or_404(
            Student,
            student_id=student.student_id,
            course=course
        )
        enrolments = set([
            e.unit.unit_code for e in student.enrolment_set.all() if e.has_passed
        ])
        core_lists = [
            set([c.unit.unit_code for c in cl.core_set.all()])
            for cl in course.corelist_set.all()
        ]
        missing_cores = min(list(
            map(lambda x: x.difference(enrolments), core_lists)
        ), key=lambda x: len(x))
        if len(missing_cores) <= 0:
            student.has_graduated = True
            student.save()
        # res[id] = (student.has_graduated, str(missing_cores))
        res[student] = (course, missing_cores)
    return res
