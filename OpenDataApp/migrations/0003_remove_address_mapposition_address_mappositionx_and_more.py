# Generated by Django 4.0.2 on 2022-02-18 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OpenDataApp', '0002_rename_image_gallery_general'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='mapposition',
        ),
        migrations.AddField(
            model_name='address',
            name='mappositionX',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='mappositionY',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
