# Generated by Django 2.2.8 on 2019-12-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("municipales", "0008_renommer_liste_en_strategy")]

    operations = [
        migrations.AlterField(
            model_name="communepage",
            name="strategy",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Stratégie"
            ),
        )
    ]
