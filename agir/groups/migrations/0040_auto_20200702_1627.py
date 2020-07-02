# Generated by Django 2.2.14 on 2020-07-02 14:27

import django.core.validators
from django.db import migrations
import dynamic_filenames
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0039_auto_20200701_1622"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supportgroup",
            name="image",
            field=stdimage.models.StdImageField(
                blank=True,
                help_text="Vous pouvez ajouter une image de bannière : elle apparaîtra sur la page, et sur les réseaux sociaux en cas de partage. Préférez une image à peu près deux fois plus large que haute. Elle doit faire au minimum 1200 pixels de large et 630 de haut pour une qualité optimale.",
                upload_to=dynamic_filenames.FilePattern(
                    filename_pattern="{app_label}/{model_name}/{instance.id}/banner{ext}"
                ),
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "gif", "png", "svg"]
                    )
                ],
                verbose_name="image",
            ),
        ),
    ]
