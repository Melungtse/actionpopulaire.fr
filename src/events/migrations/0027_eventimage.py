# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import events.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0023_auto_20171129_1824'),
        ('events', '0026_add_report_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', stdimage.models.StdImageField(upload_to=events.models.upload_to_event_directory_uuid, verbose_name='Fichier')),
                ('legend', models.CharField(max_length=280, verbose_name='légende')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_images', to='people.Person')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='events.Event')),
            ],
        ),
    ]
