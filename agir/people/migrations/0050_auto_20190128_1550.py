# Generated by Django 2.1.5 on 2019-01-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("people", "0049_auto_20190114_1551")]

    operations = [
        migrations.AddField(
            model_name="person",
            name="location_citycode",
            field=models.CharField(
                blank=True, max_length=20, verbose_name="code INSEE"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="coordinates_type",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Coordonnées manuelles"),
                    (10, "Coordonnées automatiques précises"),
                    (20, "Coordonnées automatiques approximatives (niveau rue)"),
                    (25, "Coordonnées automatique approximatives (arrondissement)"),
                    (30, "Coordonnées automatiques approximatives (ville)"),
                    (50, "Coordonnées automatiques (qualité inconnue)"),
                    (254, "Pas de position géographique"),
                    (255, "Coordonnées introuvables"),
                ],
                editable=False,
                help_text="Comment les coordonnées ci-dessus ont-elle été acquises",
                null=True,
                verbose_name="type de coordonnées",
            ),
        ),
    ]