# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_userattributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicegroupadmins',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='registration.DeviceGroup'),
        ),
    ]