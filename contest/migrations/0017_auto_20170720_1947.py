# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-20 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_contestproblem_spj_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_system',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='subtask',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='subtask_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contestrank',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]