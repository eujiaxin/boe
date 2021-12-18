import os
import time
from api.models import Student, Course, Unit, Enrolment
from django.shortcuts import get_object_or_404
from functools import lru_cache


@lru_cache(maxsize=2048)
def fetch_student(student_id):
    return get_object_or_404(
        Student,
        student_id=student_id
    )


def validate_graduation(student):
    pass
