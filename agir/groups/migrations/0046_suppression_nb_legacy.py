# Generated by Django 3.1.3 on 2021-01-06 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0045_transferoperation"),
    ]

    operations = [
        migrations.RemoveIndex(model_name="supportgroup", name="groups_nb_path_index",),
        migrations.RemoveField(model_name="supportgroup", name="location_address",),
        migrations.RemoveField(model_name="supportgroup", name="nb_id",),
        migrations.RemoveField(model_name="supportgroup", name="nb_path",),
    ]