# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-06 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0013_auto_20160404_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='spj_version',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
