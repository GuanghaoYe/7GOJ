# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-29 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0006_auto_20170729_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
