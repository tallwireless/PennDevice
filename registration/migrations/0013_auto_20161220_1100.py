# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 16:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_devicegroup_admins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicegroupadmins',
            name='admins',
        ),
        migrations.RemoveField(
            model_name='devicegroupadmins',
            name='group',
        ),
        migrations.DeleteModel(
            name='DeviceGroupAdmins',
        ),
    ]
