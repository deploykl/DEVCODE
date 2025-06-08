from django.db import models


class Patrimonio(models.Model):
    # Identificación
    usuario = models.CharField(
        "Usuario asignado", max_length=100, blank=True, null=True
    )
    ubicacion = models.CharField(
        "Ubicación física", max_length=100, blank=True, null=True
    )

    # Códigos de inventario
    codigo_2024 = models.CharField("Código 2024", max_length=50, blank=True, null=True)
    codigo_ant = models.CharField(
        "Código anterior", max_length=50, blank=True, null=True
    )
    codigo_sbn = models.CharField("Código SBN", max_length=50, blank=True, null=True)
    codigo = models.CharField("Código interno", max_length=50, blank=True, null=True)

    # Descripción del equipo
    denominacion = models.CharField(
        "Denominación", max_length=200, blank=True, null=True
    )
    detalle = models.TextField("Detalle adicional", blank=True, null=True)

    # Especificaciones técnicas
    marca = models.CharField("Marca", max_length=100, blank=True, null=True)
    modelo = models.CharField("Modelo", max_length=100, blank=True, null=True)
    serie = models.CharField("Número de serie", max_length=100, blank=True, null=True)
    dimensiones = models.CharField("Dimensiones", max_length=100, blank=True, null=True)
    color = models.CharField("Color", max_length=50, blank=True, null=True)

    # Metadatos
    fecha_adquisicion = models.DateField("Fecha de adquisición", blank=True, null=True)
    valor_actual = models.DecimalField(
        "Valor actual", max_digits=10, decimal_places=2, blank=True, null=True
    )
    estado = models.CharField("Estado", max_length=20, blank=True, null=True)
    observaciones = models.TextField("Observaciones", blank=True, null=True)

    class Meta:
        verbose_name = "Equipo de patrimonio informático"
        verbose_name_plural = "Equipos de patrimonio informático"
        ordering = ["codigo_2024", "denominacion"]
        db_table = "patrimonio_informatico"

    def __str__(self):
        return f"{self.codigo_2024 or 'Sin código'} - {self.denominacion or 'Sin denominación'}"
