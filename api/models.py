import os
from django.conf import settings
from django.db import models
from functools import reduce

from django.db.models.deletion import CASCADE

SEMESTER_CHOICE = [
    ("1", "Semester 1"),
    ("2", "Semester 2"),
    ("3", "October Semester")
]

GRADE_CHOICE = [
    ('HD', 'High Distinction'),
    ('D', 'Distinction'),
    ('C', 'Credit'),
    ('P', 'Pass'),
    ('N', 'Fail'),
    ('DEF', 'Deferred Assessment'),
    ('E', 'Exempt'),
    ('HI', 'First Class Honours'),
    ('HIIA', 'Second Class Honours Division A'),
    ('HIIB', 'Second Class Honours Division B'),
    ('NA', 'Not Applicable'),
    ('NAS', 'Non-Assessed'),
    ('NE', 'Not Examinable'),
    ('NGO', 'Fail'),
    ('NH', 'Hurdle Fail'),
    ('NS', 'Supplementary Assessment Granted'),
    ('NSR', 'Not Satisfied Requirements'),
    ('PGO', 'Pass Grade Only (no higher grade available)'),
    ('SFR', 'Satisfied Faculty Requirements'),
    ('WDN', 'Withdrawn'),
    ('WH', 'Withheld'),
    ('WI', 'Withdrawn Incomplete'),
    ('WN', 'Withdrawn Fail')
]

COURSEMODULE_TYPE = (
    ('D', 'default'),
    ('S', 'Specialisation'),
    ('MJ', 'Major'),
    ('MN', 'Minor'),
)


class Student(models.Model):
    student_id = models.CharField(
        max_length=128,
        verbose_name="Student ID"
    )
    course = models.ForeignKey(
        to="Course",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Course in which the Student is enrolled in"
    )
    student_name = models.CharField(
        max_length=256, verbose_name="Student's Name"
    )
    student_email = models.EmailField(  # Can build custom validator for monash emails
        max_length=128,
        verbose_name="Student Email",
        null=True
    )
    student_intake_year = models.PositiveSmallIntegerField(
        verbose_name="Student's Intake Year"
    )
    student_intake_semester = models.CharField(  # not sure if should use charfield
        max_length=64,
        choices=SEMESTER_CHOICE,
        null=True,
        verbose_name="Student's First Semester Intake"
    )
    has_graduated = models.BooleanField(verbose_name="Have Student Graduated?")

    class Meta:
        unique_together = [['student_id', 'course']]
        ordering = ['course', 'student_id']
        verbose_name = 'student'
        verbose_name_plural = 'students'
        indexes = [
            models.Index(fields=['student_id', 'course', ]),
        ]

    def get_completed_units(self):
        return set([
            e.unit for e in self.enrolment_set.all() if e.has_passed
        ])

    def validate_graduation(self):
        completed_units = self.get_completed_units()
        ret = []
        for cm in self.course.coursemodule_set.all():
            missing_cores, remaining, has_completed_core = cm.process_core(
                completed_units
            )
            missing_credits, _, has_completed_elective = cm.process_elective(
                remaining
            )
            status = has_completed_core and has_completed_elective
            ret.append((cm.cm_code, missing_cores, missing_credits, status))
        return ret

    def __str__(self):
        return f'Student: {self.student_id} {self.student_name}'


class Course(models.Model):
    course_code = models.CharField(
        max_length=16, verbose_name="Course Code"
    )
    course_version = models.PositiveSmallIntegerField(
        null=True,
        default=None,
        verbose_name="Course Version"
    )
    faculty = models.ForeignKey(
        to='Faculty',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Faculty in which the Course belongs to"
    )
    course_name = models.CharField(
        max_length=256, verbose_name="Course Name"
    )
    course_required_credits = models.PositiveSmallIntegerField(
        verbose_name="Total Credits Requried to Complete this Course"
    )
    course_duration_limit = models.PositiveSmallIntegerField(
        default=8,
        verbose_name="Maximum Years to Complete this Course"
    )

    class Meta:
        ordering = ['faculty', 'course_code']
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        unique_together = [['course_code', 'course_version']]
        indexes = [
            models.Index(fields=['course_code', 'course_version'])
        ]

    # def save(self, *args, **kwargs):
    #     if not Course.objects.filter(pk=self.pk).exists():
    #         self.course_version = max([
    #             x.course_version for x in Course.objects.filter(course_name=self.course_name)
    #         ] + [0]) + 1
    #     super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f'Course: {self.course_code}.v{self.course_version}'


class CourseModule(models.Model):
    cm_code = models.CharField(
        max_length=32,
        verbose_name="Course Module Code",
        unique=True
    )
    cm_name = models.CharField(
        max_length=128,
        verbose_name="Course Module Name"
    )
    course = models.ForeignKey(
        to="Course",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Course in which the CourseModule belongs to"
    )
    type = models.CharField(
        max_length=64,
        choices=COURSEMODULE_TYPE,
        null=False,
        verbose_name="Course Module Type"
    )
    required_elective_credit_points = models.PositiveSmallIntegerField(
        verbose_name="Course Module required credit points"
    )

    def process_core(self, units):
        core_lists = [
            set(core.unit for core in cl.core_set.all()) for cl in self.corelist_set.all()
        ]

        assert sum([1 for _ in range(core_lists)]
                   ) == 1, 'core list should always only have one nested list (as of implementation logic now)'

        has_completed = False
        missing_cores, min_cl = min(
            map(
                lambda x: (x.difference(units), x), core_lists
            ), key=lambda x: len(x)
        )
        if len(missing_cores) <= 0:
            has_completed = True
        # FIXME : length of core list may be inconsistent!
        remaining = units.difference(min_cl)
        return list(missing_cores), remaining, has_completed

    def process_elective(self, units):
        elective_lists = [
            None if el.elective_set.is_free else [  # FIXME
                elective for elective in el.elective_set.all()
            ]
            for el in self.electivelist_set.all()
        ]
        has_completed = False
        credits_earned, max_el = max(map(
            lambda x: (reduce(
                lambda acc, u: acc + u.unit_credits,
                units.intersection(x) if x else units  # FIXME
            ), x), elective_lists
        ))
        if credits_earned >= self.required_elective_credit_points:
            has_completed = True
        return self.required_elective_credit_points - credits_earned, units.difference(max_el), has_completed

    def __str__(self):
        return f'CourseModule: {self.cm_code} - {self.cm_name}'


class CoreList(models.Model):
    course_module = models.ForeignKey(
        to="CourseModule",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Core list'
        verbose_name_plural = 'Core lists'

    def __str__(self):
        return f'Core List: {self.pk} - {self.course_module}'


class ElectiveList(models.Model):
    course_module = models.ForeignKey(
        to="CourseModule",
        on_delete=models.CASCADE
    )
    is_free = models.BooleanField(
        default=False,
        null=True,
        verbose_name="is free elective"
    )

    class Meta:
        verbose_name = 'Elective list'
        verbose_name_plural = 'Elective lists'

    def __str__(self):
        return f'Elective List: {self.pk} - {self.course_module}'


class Core(models.Model):
    core_list = models.ForeignKey(
        to="CoreList",
        on_delete=models.CASCADE
    )
    unit = models.ForeignKey(
        to="Unit",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [['core_list', 'unit']]
        ordering = ['core_list', 'unit']
        verbose_name = 'core'
        verbose_name_plural = 'cores'

    def __str__(self):
        return f'Core: {self.core_list} - {self.unit}'


class Elective(models.Model):
    elective_list = models.ForeignKey(
        to="ElectiveList",
        on_delete=models.CASCADE
    )
    unit = models.ForeignKey(
        to="Unit",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [['elective_list', 'unit']]
        ordering = ['elective_list', 'unit']
        verbose_name = 'elective'
        verbose_name_plural = 'electives'

    def __str__(self):
        return f'Elective: {self.elective_list} - {self.unit}'


class Unit(models.Model):
    unit_code = models.CharField(
        max_length=32,
        verbose_name="Unit Code",
        unique=True
    )
    faculty = models.ForeignKey(
        to="Faculty",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Faculty Responsible for the Unit"
    )
    unit_name = models.CharField(
        max_length=128,
        verbose_name="Name of the Unit",
        null=True
    )
    unit_credits = models.PositiveSmallIntegerField(
        verbose_name="Credits Awarded for Completing this Unit"
    )

    class Meta:
        ordering = ['faculty', 'unit_code']
        verbose_name = 'unit'
        verbose_name_plural = 'units'
        indexes = [
            models.Index(fields=['unit_code'])
        ]

    def __hash__(self):
        print("psyche, hahahahahhash")
        return self.unit_code.__hash__()

    def __str__(self):
        return f'Unit: {self.unit_code} {self.unit_name if self.unit_name else ""}'


class Enrolment(models.Model):
    student = models.ForeignKey(
        to="Student",
        on_delete=models.CASCADE,  # cascade???
        verbose_name="Student Object in this Enrolment"
    )
    unit = models.ForeignKey(
        to="Unit",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Unit in which the Student has Enrolled in"
    )
    enrolment_year = models.PositiveSmallIntegerField(
        verbose_name="Year in which Student is Taking this Unit"
    )
    enrolment_semester = models.CharField(  # not sure if should use charfield
        max_length=64,
        choices=SEMESTER_CHOICE,
        null=True,
        verbose_name="Semester in which Student is Taking this Unit"
    )
    enrolment_marks = models.SmallIntegerField(
        null=True,
        verbose_name="Marks obtained by the Student in this Unit"
    )
    enrolment_grade = models.CharField(
        max_length=64,
        choices=GRADE_CHOICE,
        null=True,
        verbose_name="Grade obtained by the Student in this Unit"
    )
    has_passed = models.BooleanField(
        verbose_name="Has the Student Passed this Unit?",
        null=True
    )

    class Meta:
        unique_together = [
            ['student', 'unit', 'enrolment_year', 'enrolment_semester']]
        ordering = ['student', 'unit']
        verbose_name = 'enrolment'
        verbose_name_plural = 'enrolments'

    def __str__(self):
        return f'Enrolment: {self.student.student_id} - {self.unit.unit_code}'


class CallistaDataFile(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="User Generated Identifier for File"
    )
    upload = models.FileField(
        upload_to='callista/',
        verbose_name="Student Callista Data"
    )
    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date and Time the file was uploaded"
    )
    has_been_processed = models.BooleanField(
        default=False,
        verbose_name="File has been processed into Database"
    )

    class Meta:
        ordering = ['upload_date']
        verbose_name = 'callista data file'
        verbose_name_plural = 'callista data files'

    def delete(self, *args, **kwargs):
        try:
            print(
                f"deleting file at {os.path.join(settings.MEDIA_ROOT, self.upload.name)}")
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload.name))
        except FileNotFoundError:
            print(
                f"File not found at {os.path.join(settings.MEDIA_ROOT, self.upload.name)}")
            pass
        super(CallistaDataFile, self).delete(*args, **kwargs)

    def __str__(self):
        return f'File: {self.upload.name.split("/")[-1]}'


class Faculty(models.Model):
    faculty_name = models.CharField(
        max_length=64, verbose_name="Faculty Name",
        unique=True
    )

    class Meta:
        ordering = ["faculty_name"]
        verbose_name = 'faculty'
        verbose_name_plural = 'faculties'

    def __str__(self):
        return f'Faculty: {self.faculty_name}'
