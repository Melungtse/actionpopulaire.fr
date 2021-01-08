# Generated by Django 2.2.6 on 2019-11-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0001_creer_modeles"),
        ("municipales", "0004_auto_20190924_1725"),
    ]

    operations = [
        migrations.AddField(
            model_name="communepage",
            name="municipales2020_admins",
            field=models.ManyToManyField(
                blank=True,
                related_name="municipales2020_commune",
                to="people.Person",
                verbose_name="Têtes de file pour les élections municipales de 2020",
            ),
        )
    ]
