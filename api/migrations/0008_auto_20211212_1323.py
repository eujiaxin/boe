# Generated by Django 3.2.9 on 2021-12-12 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20211212_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolment',
            name='enrolment_grade',
            field=models.CharField(choices=[('HD', 'High Distinction'), ('D', 'Distinction'), ('C', 'Credit'), ('P', 'Pass'), ('N', 'Fail'), ('DEF', 'Deferred Assessment'), ('E', 'Exempt'), ('HI', 'First Class Honours'), ('HIIA', 'Second Class Honours Division A'), ('HIIB', 'Second Class Honours Division B'), ('NA', 'Not Applicable'), ('NAS', 'Non-Assessed'), ('NE', 'Not Examinable'), ('NGO', 'Fail'), ('NH', 'Hurdle Fail'), ('NS', 'Supplementary Assessment Granted'), ('NSR', 'Not Satisfied Requirements'), ('PGO', 'Pass Grade Only (no higher grade available)'), ('SFR', 'Satisfied Faculty Requirements'), ('WDN', 'Withdrawn'), ('WH', 'Withheld'), ('WI', 'Withdrawn Incomplete'), ('WN', 'Withdrawn Fail')], max_length=64, null=True, verbose_name='Grade obtained by the Student in this Unit'),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='enrolment_semester',
            field=models.CharField(choices=[('1', 'Semester 1'), ('2', 'Semester 2'), ('3', 'October Semester')], max_length=64, null=True, verbose_name='Semester in which Student is Taking this Unit'),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='has_passed',
            field=models.BooleanField(null=True, verbose_name='Has the Student Passed this Unit?'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_email',
            field=models.EmailField(max_length=128, null=True, verbose_name='Student Email'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_code',
            field=models.CharField(max_length=32, unique=True, verbose_name='Unit Code'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_name',
            field=models.CharField(max_length=128, null=True, verbose_name='Name of the Unit'),
        ),
    ]
