# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-15 10:44
from __future__ import unicode_literals

from django.db import migrations, models
import lib.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_refactoring_description_and_datetime_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='allow_html',
            field=models.BooleanField(default=False, verbose_name='autoriser le HTML étendu dans la description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=lib.models.DescriptionField(blank=True, help_text='Une courte description', verbose_name='description'),
        ),
    ]