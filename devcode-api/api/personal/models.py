from django.db import models

class Anexo(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Número")  # Asegura que el nombre sea único

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ["number"]

    def __str__(self):
        return str(self.number)  # Convertir el número a cadena
    
class Condition(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")  # Asegura que el nombre sea único

    class Meta:
        verbose_name = "Condition"
        verbose_name_plural = "Conditions"
        ordering = ["name"]

    def __str__(self):
        return self.name
        
class Dependencia(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")

    class Meta:
        verbose_name = "Dependencia"
        verbose_name_plural = "Dependencias"
        ordering = ["name"]

    def __str__(self):
        return self.name   
    
class Area(models.Model):
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE, related_name="areas")  # Relación uno a muchos
    name = models.CharField(max_length=255, verbose_name="Nombre")  # Asegura que el nombre sea único

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        ordering = ["name"]

    def __str__(self):
        return self.name

class DependenciaArea(models.Model):
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE, related_name='dependencia_areas')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='area_dependencias')

    class Meta:
        verbose_name = "Dependencia-Area"
        verbose_name_plural = "Dependencias-Areas"
        unique_together = ('dependencia', 'area')  # Asegura que la misma combinación no se repita

    def __str__(self):
        return f'{self.dependencia} - {self.area}'
    
class Profesion(models.Model):
    name = models.CharField(max_length=255, verbose_name="Profesión")

    class Meta:
        verbose_name = "Profesion"
        verbose_name_plural = "Profesiones"
        ordering = ["name"]

    def __str__(self):
        return self.name   
    
class Cargo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Cargo")

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["name"]

    def __str__(self):
        return self.name   
    
class GrupoOcupacional(models.Model):
    descripcion = models.CharField(max_length=255, verbose_name="Grupo Ocupacional")

    class Meta:
        verbose_name = "GrupoOcupacional"
        verbose_name_plural = "GrupoOcupacionales"
        ordering = ["descripcion"]

    def __str__(self):
        return self.descripcion   
    
class Estado(models.Model):
    descripcion = models.CharField(max_length=255, verbose_name="Descripcion")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ["descripcion"]

    def __str__(self):
        return self.descripcion   
    
class Generica(models.Model):
    descripcion = models.CharField(max_length=255, verbose_name="Descripcion")
    detalle = models.CharField(max_length=255, verbose_name="Detalle")

    class Meta:
        verbose_name = "Generica"
        verbose_name_plural = "Genericas"
        ordering = ["descripcion"]

    def __str__(self):
        return self.descripcion   