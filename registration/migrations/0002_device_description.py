# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
