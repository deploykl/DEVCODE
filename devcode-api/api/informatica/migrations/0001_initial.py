# Generated by Django 5.0.13 on 2025-04-01 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Informatica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=50, verbose_name='Fecha')),
                ('codigo', models.CharField(max_length=50, verbose_name='Código')),
                ('inv_2023', models.CharField(blank=True, max_length=50, null=True, verbose_name='Inventario 2023')),
                ('cod_sbn', models.CharField(blank=True, max_length=50, null=True, verbose_name='Código SBN')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('marca', models.CharField(max_length=100, verbose_name='Marca')),
                ('modelo', models.CharField(max_length=100, verbose_name='Modelo')),
                ('serie', models.CharField(max_length=100, verbose_name='Serie')),
                ('piso', models.CharField(max_length=10, verbose_name='Piso')),
                ('estado', models.CharField(max_length=20, verbose_name='Estado')),
                ('usuario', models.CharField(max_length=100, verbose_name='Usuario')),
                ('user', models.CharField(max_length=50, verbose_name='User')),
                ('condicion', models.CharField(max_length=20, verbose_name='Condición')),
                ('dependencia', models.CharField(max_length=50, verbose_name='Dependencia')),
                ('area', models.CharField(max_length=50, verbose_name='Área')),
                ('responsable', models.CharField(max_length=100, verbose_name='Responsable')),
                ('ape_res', models.CharField(max_length=100, verbose_name='Apellidos Responsable')),
                ('nom_res', models.CharField(max_length=100, verbose_name='Nombres Responsable')),
                ('user_res', models.CharField(max_length=50, verbose_name='User Responsable')),
                ('condicion1', models.CharField(max_length=20, verbose_name='Condición Responsable')),
                ('dependencia1', models.CharField(max_length=50, verbose_name='Dependencia Responsable')),
                ('area1', models.CharField(max_length=50, verbose_name='Área Responsable')),
                ('observacion', models.TextField(blank=True, null=True, verbose_name='Observación')),
            ],
            options={
                'verbose_name': 'Equipo de Informática',
                'verbose_name_plural': 'Equipos de Informática',
                'ordering': ['piso', 'codigo'],
            },
        ),
    ]
