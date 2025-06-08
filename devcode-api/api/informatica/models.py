from django.db import models

class Informatica(models.Model):
    # Campos del equipo
    fecha = models.CharField("Fecha", max_length=50, blank=True, null=True)  # Ejemplo: "2024-08-07 11:07:05"
    codigo = models.CharField("Código", max_length=50, blank=True, null=True)
    inv_2023 = models.CharField("Inventario 2023", max_length=50, blank=True, null=True)
    cod_sbn = models.CharField("Código SBN", max_length=50, blank=True, null=True)
    descripcion = models.CharField("Descripción", max_length=200, blank=True, null=True)
    marca = models.CharField("Marca", max_length=100, blank=True, null=True)
    modelo = models.CharField("Modelo", max_length=100, blank=True, null=True)
    serie = models.CharField("Serie", max_length=100, blank=True, null=True)
    piso = models.CharField("Piso", max_length=10, blank=True, null=True)
    condicion = models.CharField("Condición", max_length=20, blank=True, null=True)  # Sin choices
    antiguedad = models.CharField("Antiguedad", max_length=4, blank=True, null=True)  # Cambiado a max_length=4
    con_equipo = models.CharField("Condición Equipo", max_length=20, blank=True, null=True)  # Sin choices

    # Campos del usuario asignado
    usuario = models.CharField("Usuario", max_length=100, blank=True, null=True)
    user = models.CharField("User", max_length=50, blank=True, null=True)
    estado = models.CharField("Estado", max_length=20, blank=True, null=True)  # Sin choices
    dependencia = models.CharField("Dependencia", max_length=50, blank=True, null=True)
    area = models.CharField("Área", max_length=50, blank=True, null=True)
    
    # Campos del responsable
    responsable = models.CharField("Responsable", max_length=100, blank=True, null=True)
    user_res = models.CharField("User Responsable", max_length=50, blank=True, null=True)
    condicion1 = models.CharField("Condición Responsable", max_length=20, blank=True, null=True)  # Sin choices
    dependencia1 = models.CharField("Dependencia Responsable", max_length=50, blank=True, null=True)
    area1 = models.CharField("Área Responsable", max_length=50)
    observacion = models.TextField("Observación", blank=True, null=True)

    class Meta:
        verbose_name = "Equipo de Informática"
        verbose_name_plural = "Equipos de Informática"
        ordering = ["piso", "codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion} ({self.piso})"