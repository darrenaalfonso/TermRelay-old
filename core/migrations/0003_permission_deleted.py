# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-13 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170613_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
