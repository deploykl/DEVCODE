# Generated by Django 5.0.13 on 2025-04-04 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0015_area_dependencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Profesión')),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Profesión')),
            ],
            options={
                'verbose_name': 'Profesion',
                'verbose_name_plural': 'Profesiones',
                'ordering': ['name'],
            },
        ),
    ]
