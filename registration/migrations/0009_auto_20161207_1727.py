# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20161207_1726'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PennUser',
        ),
        migrations.AlterField(
            model_name='devicegroup',
            name='personal',
            field=models.BooleanField(default=False),
        ),
    ]
