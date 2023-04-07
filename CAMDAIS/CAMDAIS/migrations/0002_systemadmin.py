# Generated by Django 4.0.4 on 2023-04-07 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CAMDAIS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='systemAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CAMDAIS.institute')),
            ],
        ),
    ]
