import os
import pandas as pd
from api.models import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from scripts.delete_db import run as clear_db


def run():
    clear_db()
    script_path = os.path.join(settings.BASE_DIR, "scripts")
    df = pd.read_csv(os.path.join(script_path, "cs_course_data_2.csv"))

    for unit_code in list(df["UNIT_CODE"].unique()):
        Unit.objects.create(
            unit_code=unit_code,
            unit_credits=6
        )

    c2001 = Course.objects.create(
        course_code='C2001',
        course_version='1',
        course_name='Bachelor of Computer Science',
        free_elective_credits=48,
        course_duration_limit=8
    )

    wrapper1 = c2001.wrapper_set.create(
        threshold=1,
        parent=None,
        is_leaf=False,
        required_core_credit_points=42
    )

    cm1 = wrapper1.coursemodule_set.create(
        cm_code='C2001AB',
        cm_name='C2001AB',
        type='default'
    )

    cl1 = cm1.corelist_set.create()

    lst = ["FIT1008", "FIT1045", "FIT1047",
           "FIT2004", "FIT2014", "MAT1830", "MAT1841"]

    for unit_code in lst:
        _ = cl1.core_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    el1 = cm1.electivelist_set.create(
        required_elective_credit_points=6
    )

    lst = ["FIT1049", "FIT1055"]

    for unit_code in lst:
        _ = el1.elective_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    wrapper2 = Wrapper.objects.create(
        threshold=1,
        parent=wrapper1,
        is_leaf=False,
        required_core_credit_points=42
    )

    cm2 = wrapper2.coursemodule_set.create(
        cm_code='COMPSCI03',
        cm_name='Advanced computer science',
        type='Specialisation'
    )

    cl2 = cm2.corelist_set.create()

    lst = ["FIT2099", "FIT2102", "FIT3143",
           "FIT3155", "FIT3171", "FIT3161", "FIT3162"]

    for unit_code in lst:
        _ = cl2.core_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    el2 = cm2.electivelist_set.create(
        required_elective_credit_points=6
    )

    lst = ["FIT3031", "FIT3077", "FIT3080", "FIT3081",
           "FIT3088", "FIT3094", "FIT3139", "FIT3142",
           "FIT3146", "FIT3152", "FIT3159", "FIT3165",
           "FIT3173", "FIT3175", "FIT3181", "FIT3182",
           "FIT3183", "MTH3170", "MTH3175"]

    for unit_code in lst:
        print(unit_code)
        _ = el2.elective_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    cm3 = wrapper2.coursemodule_set.create(
        cm_code='DATASCI01',
        cm_name='Data science',
        type='Specialisation'
    )

    cl3 = cm3.corelist_set.create()

    lst = ["FIT1043", "FIT2086", "FIT2094",
           "FIT3179", "FIT3163", "FIT3164"]

    for unit_code in lst:
        print(unit_code)
        _ = cl3.core_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    el3 = cm3.electivelist_set.create(
        required_elective_credit_points=6
    )

    lst = ["FIT3003", "FIT3139", "FIT3152", "FIT3154",
           "FIT3181", "FIT3182", "FIT3183"]

    for unit_code in lst:
        _ = el3.elective_set.create(
            unit=Unit.objects.get(unit_code=unit_code)
        )

    wrapper3 = Wrapper.objects.create(
        threshold=1,
        parent=wrapper2,
        is_leaf=True,
        required_core_credit_points=6
    )

    cm4 = wrapper3.coursemodule_set.create(
        cm_code='C2001E_IBL',
        cm_name='C2001E_IBL',
        type='default'
    )

    cm5 = wrapper3.coursemodule_set.create(
        cm_code='C2001E_IWE',
        cm_name='C2001E_IWE',
        type='default'
    )

    lst = ["FIT2099", "FIT2102", "FIT3143",
           "FIT3155", "FIT3171"]

    cl4 = cm4.corelist_set.create()

    cl5 = cm5.corelist_set.create()

    _ = cl4.core_set.create(
        unit=Unit.objects.get(unit_code="FIT3045")
    )

    _ = cl5.core_set.create(
        unit=Unit.objects.get(unit_code="FIT3199")
    )
