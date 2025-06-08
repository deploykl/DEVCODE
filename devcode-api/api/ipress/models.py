from django.db import models

# Create your models here.
# Create your models here.
class Ipress(models.Model):
    codigo = models.CharField(max_length=150, verbose_name="Código")
    institucion = models.CharField(max_length=150, verbose_name="Institución")
    departamento = models.CharField(max_length=150, verbose_name="Departamento")
    provincia = models.CharField(max_length=150, null=False, verbose_name="Provincia")
    distrito = models.CharField(max_length=150, null=False, verbose_name="Distrito")
    disa = models.CharField(max_length=150, null=False, verbose_name="Disa")
    categoria = models.CharField(max_length=150, null=False, verbose_name="Categoría")
    establecimiento = models.CharField(max_length=300, null=False, verbose_name="Establecimiento")

    def __str__(self):
        return self.establecimiento
