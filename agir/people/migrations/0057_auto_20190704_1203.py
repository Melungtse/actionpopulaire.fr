# Generated by Django 2.2.2 on 2019-07-04 10:03

import agir.lib.form_fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("people", "0056_auto_20190521_1702")]

    operations = [
        migrations.AlterField(
            model_name="personformsubmission",
            name="data",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=dict,
                encoder=agir.lib.form_fields.CustomJSONEncoder,
                verbose_name="Données",
            ),
        ),
        migrations.AlterField(
            model_name="personformsubmission",
            name="person",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="form_submissions",
                to="people.Person",
            ),
        ),
    ]
