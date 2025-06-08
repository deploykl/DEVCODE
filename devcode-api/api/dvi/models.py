from django.db import models

class Direccion(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")

class Meta(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")
    
class Situacion(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")

    