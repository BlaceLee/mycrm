# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-08-17 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_permission_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='url_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
