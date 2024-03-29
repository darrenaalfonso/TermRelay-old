# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-22 03:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_permission_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='product',
            name='deleted',
        ),
        migrations.AddField(
            model_name='inquiry',
            name='inquiry_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='productquestionchoice',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productquestionchoice',
            name='numerical_answer',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='productquestionchoice',
            name='numerical_answer_units',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='productquestionchoice',
            name='text_answer',
            field=models.TextField(blank=True, null=True),
        ),
    ]
