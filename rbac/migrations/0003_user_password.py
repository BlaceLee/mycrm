# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-08-12 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20200812_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='123', max_length=64),
        ),
    ]
