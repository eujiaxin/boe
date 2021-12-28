import os
from django.conf import settings
from django.db import models
from functools import reduce
from django.db.models.base import ModelStateFieldsCacheDescriptor

from django.db.models.deletion import CASCADE, SET_NULL

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
        """
        return (remaining_units, most_completed_cm) if pass
        return (remaining_units, most_completed_cm, missing_cores, missing_credits, depth) if fail
        """
        completed_units = self.get_completed_units()
        ret = []
        self.traverse_wrapper(self.course, completed_units, 0, ret)
        completion = list(filter(lambda x: len(x) == 2, ret))
        if completion:
            return completion[0]
        return ret

    def traverse_wrapper(self, wrapper, units, depth, part):
        if wrapper.wrapper_set.all():
            for child in wrapper.wrapper_set.all():
                # (status, remaining_units, most_completed_cm, missing_cores, missing_credits)
                tup = child.is_complete(units)
                if tup[0]:
                    if not child.wrapper_set.all():
                        # two items only when successfully end
                        part.append((tup[1], tup[2]))
                    else:
                        self.traverse_wrapper(child, tup[1], depth+1, part)
                else:
                    part.append((tup[1], tup[2], tup[3], tup[4], depth))

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
    #             x.course_version for x in Course.objects.course_name=self.course_name)
    #         ] + [0]) + 1
    #     super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f'Course: {self.course_code}.v{self.course_version}'


class Wrapper(models.Model):
    course = models.ForeignKey(
        to="Course",
        on_delete=models.SET_NULL,
        null=True
    )
    threshold = models.PositiveSmallIntegerField()
    parent = models.ForeignKey(
        to="Wrapper",
        null=True,
        on_delete=models.CASCADE
    )
    is_leaf = models.BooleanField(
        default=False,
        null=False
    )
    required_core_credit_points = models.PositiveSmallIntegerField(
        verbose_name="Wrapper required core credit points"
    )

    class Meta:
        verbose_name = 'wrapper'
        verbose_name_plural = 'wrappers'

    def is_complete(self, units):
        """(status, remaining_units, most_completed_cm, missing_cores, missing_credits)"""
        core_complete, remaining, most_completed_core_cm, missing_cores, missing_core_credits = self.core_passed(
            units)
        electives_complete, remaining, most_completed_cm, missing_elective_credits = self.electives_passed(
            remaining, most_completed_core_cm)
        return core_complete and electives_complete, \
            remaining, most_completed_cm, missing_cores, \
            missing_core_credits+missing_elective_credits

    def core_passed(self, units):
        """(status, remaining units, most_completed_cm, missing cores, missing credits)"""
        cm_cores = [(*cm.process_core(units), cm)
                    for cm in self.coursemodule_set.all()]
        completed_cm_cores = list(filter(lambda tup: tup[2], cm_cores))
        if len(completed_cm_cores) >= self.threshold:
            cores_taken = reduce(
                lambda acc, s: acc.union(s[1]),
                completed_cm_cores, set()
            )
            total_core_credits = reduce(
                lambda acc, u: acc + u.unit_credits,
                cores_taken, 0
            )
            most_completed_cm = list(map(lambda x: x[3], completed_cm_cores))
            if total_core_credits >= self.required_core_credit_points:
                return True, units.difference(cores_taken), most_completed_cm, None, 0
            else:
                missing_credits = self.required_core_credit_points - total_core_credits
                return False, units.difference(cores_taken), most_completed_cm, None, missing_credits
        else:
            missing_cores, cores_taken, most_completed_cm = reduce(
                lambda acc, s: (
                    acc[0].union(s[0]), acc[1].union(s[1]), acc[2]+[s[3]]
                ),
                sorted(cm_cores, key=lambda x: len(x[0]))[
                    :self.threshold],  # FIXME (MAYBE)
                (set(), set(), [])
            )
            total_core_credits = reduce(
                lambda acc, u: acc + u.unit_credits,
                cores_taken, 0
            )
            remaining = units.difference(cores_taken)
            missing_credits = self.required_core_credit_points - total_core_credits
            print("c", most_completed_cm)
            return False, remaining, most_completed_cm, missing_cores, missing_credits

    def electives_passed(self, units, most_completed_cm):
        """(status, remaining units, most_completed_cm, missing credits)"""
        cm_electives = [(*cm.process_elective(units), cm)
                        for cm in most_completed_cm]
        passed_electives = list(filter(lambda tup: tup[2], cm_electives))
        if len(passed_electives) >= self.threshold:
            electives_taken = reduce(
                lambda acc, tup: acc.union(tup[1]),
                cm_electives, set()
            )
            most_completed_electives_cm = list(
                map(lambda x: x[3], passed_electives))
            return True, units.difference(electives_taken), most_completed_electives_cm, 0
        else:
            missing_credits, electives_taken, most_completed_electives_cm = reduce(
                lambda acc, s: (
                    acc[0] + s[0], acc[1].union(s[1]), acc[2].append(s[3])
                ),
                sorted(cm_electives, key=lambda x: x[0])[:self.threshold],
                (0, set(), [])
            )
            remaining = units.difference(electives_taken)
            return False, remaining, most_completed_electives_cm, missing_credits

    def __str__(self):
        return f'Wrapper: {self.pk} - {self.course}'


class CourseModule(models.Model):
    wrapper = models.ManyToManyField(Wrapper)
    cm_code = models.CharField(
        max_length=32,
        verbose_name="Course Module Code",
        unique=True
    )
    cm_name = models.CharField(
        max_length=128,
        verbose_name="Course Module Name"
    )
    type = models.CharField(
        max_length=64,
        choices=COURSEMODULE_TYPE,
        null=False,
        verbose_name="Course Module Type"
    )

    def process_core(self, units):
        """ (cores not completed yet, cores taken, status) """
        core_lists = [
            set(core.unit for core in cl.core_set.all())
            for cl in self.corelist_set.all()
        ]

        has_completed = False
        missing_cores, most_completed_cl = min(
            map(
                lambda x: (x.difference(units), x), core_lists
            ), key=lambda x: len(x[0])
        )
        if len(missing_cores) <= 0:
            has_completed = True
        return list(missing_cores), most_completed_cl.intersection(units), has_completed

    def process_elective(self, units, is_free=False):
        """ (missing credits, electives taken, status) """
        elective_lists = [
            ([elective.unit for elective in el.elective_set.all()],
             el.required_elective_credit_points)
            for el in self.electivelist_set.all()
        ]
        has_completed = True
        electives_taken = set()
        missing_elective_credits = 0
        for unit_list, required_credits in elective_lists:
            credits_earned, electives_set = 0, set()
            for u in set(unit_list).intersection(units):  # FIXME?
                credits_earned += u.unit_credits
                electives_set.add(u)
                if credits_earned >= required_credits:
                    break
            electives_taken = electives_taken.union(electives_set)
            if credits_earned < required_credits:
                has_completed = False
                missing_elective_credits += (required_credits - credits_earned)
        return missing_elective_credits, electives_taken, has_completed

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
    required_elective_credit_points = models.PositiveSmallIntegerField(
        verbose_name="Course Module required elective credit points"
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
