# Generated by Django 4.0.4 on 2023-04-08 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CAMDAIS', '0004_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('question', models.CharField(max_length=150)),
                ('rightAns', models.CharField(max_length=150)),
                ('ans2', models.CharField(max_length=150)),
                ('ans3', models.CharField(max_length=150)),
                ('ans4', models.CharField(max_length=150)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CAMDAIS.classes')),
            ],
        ),
    ]
