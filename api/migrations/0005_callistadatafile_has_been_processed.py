# Generated by Django 3.2.9 on 2021-12-10 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20211210_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='callistadatafile',
            name='has_been_processed',
            field=models.BooleanField(default=False, verbose_name='File has been processed into Database'),
            preserve_default=False,
        ),
    ]