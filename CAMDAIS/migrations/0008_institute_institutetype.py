# Generated by Django 4.0.4 on 2023-05-19 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAMDAIS', '0007_currentgeneraltest'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='instituteType',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]