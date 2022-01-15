import os
import pandas as pd
from api.models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from scripts.delete_db import run as clear_db


def read_units_from_text_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines


def run():
    clear_db()

    script_path = os.path.join(settings.BASE_DIR, "scripts")

    units_a = read_units_from_text_file(
        os.path.join(script_path, "s2008_a.txt"))
    units_b = read_units_from_text_file(
        os.path.join(script_path, "s2008_b.txt"))
    units_c = read_units_from_text_file(
        os.path.join(script_path, "s2008_c.txt"))

    # add units to database
    for unit_code in units_a + units_b + units_c:
        Unit.objects.create(
            unit_code=unit_code,
            unit_credits=6
        )

    s2008 = Course.objects.create(
        course_code='S2008',
        course_version='1',
        course_name='Bachelor of Medical Bioscience',
        free_elective_credits=12,
        course_duration_limit=8
    )

    wrapper1 = s2008.wrapper_set.create(
        threshold=1,
        parent=None,
        is_leaf=False,
        required_core_credit_points=72
    )

    cm1 = wrapper1.coursemodule_set.create(
        cm_code='S2008_A',
        cm_name='Part A. Foundation biomedical sciences and scientific practice',
        type='default'
    )

    cl1 = cm1.corelist_set.create()

    for unit_code in units_a:
        _ = cl1.core_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    wrapper2 = Wrapper.objects.create(
        threshold=1,
        parent=wrapper1,
        is_leaf=False,
        required_core_credit_points=42
    )

    cm2 = wrapper2.coursemodule_set.create(
        cm_code='S2008_B',
        cm_name='Part B. Human health',
        type='default'
    )

    cl2 = cm2.corelist_set.create()

    for unit_code in units_b:
        _ = cl2.core_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    # el2 = cm2.electivelist_set.create(
    #     required_elective_credit_points=6
    # )

    # lst = ["FIT3031", "FIT3077", "FIT3080", "FIT3081",
    #        "FIT3088", "FIT3094", "FIT3139", "FIT3142",
    #        "FIT3146", "FIT3152", "FIT3159", "FIT3165",
    #        "FIT3173", "FIT3175", "FIT3181", "FIT3182",
    #        "FIT3183", "MTH3170", "MTH3175"]

    # for unit_code in lst:
    #     print(unit_code)
    #     _ = el2.elective_set.create(
    #         unit=Unit.objects.get(unit_code=unit_code)
    #     )

    wrapper3 = Wrapper.objects.create(
        threshold=1,
        parent=wrapper2,
        is_leaf=True,
        required_core_credit_points=6
    )

    cm3 = wrapper3.coursemodule_set.create(
        cm_code='S2008_C',
        cm_name='Part C. Internship',
        type='default'
    )

    cl3 = cm3.corelist_set.create()

    for unit_code in units_c:
        _ = cl3.core_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )
