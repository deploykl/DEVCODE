# Generated by Django 5.0.13 on 2025-04-04 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0016_cargo_profesion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Cargo'),
        ),
    ]
