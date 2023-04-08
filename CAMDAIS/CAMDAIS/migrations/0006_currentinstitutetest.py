# Generated by Django 4.0.4 on 2023-04-08 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CAMDAIS', '0005_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='currentInstituteTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CAMDAIS.classes')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CAMDAIS.institute')),
            ],
        ),
    ]