from django.db import models
from api.personal.models import *
from api.user.models import User
from api.poi.choices import TIPO_CHOICES, TRAZABILIDAD_CHOICES
from django.contrib.auth.models import Group

class Grupo(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Guardamos la instancia del modelo Grupo
        super(Grupo, self).save(*args, **kwargs)

        # Intentamos obtener el grupo existente por su nombre
        group, created = Group.objects.get_or_create(name=self.name)
        if not created:
            # Si el grupo ya existe, solo actualizamos su nombre si es necesario
            # Note: `Group` doesn't have an ID or `name` change method, so we need to handle this differently.
            if group.name != self.name:
                group.name = self.name
                group.save()  # Update the existing group name
        # Note: If created is True, a new group is created with the same name

    def delete(self, *args, **kwargs):
        # Sincronizamos la eliminación con el modelo Group de Django
        try:
            group = Group.objects.get(name=self.name)
            group.delete()
        except Group.DoesNotExist:
            # Si el grupo no existe, no hacemos nada
            pass
        # Elimina la instancia del modelo Grupo
        super(Grupo, self).delete(*args, **kwargs)
    
class MedidaActividad(models.Model):
    codigo = models.CharField(max_length=150, verbose_name="Código")
    name = models.CharField(max_length=500, verbose_name="Nombre")

    def __str__(self):
        return f"{self.codigo} , {self.name}"
    
class Actividad(models.Model):
    codigo = models.CharField(max_length=150,verbose_name="Código", blank=True, null=True)
    name = models.CharField(max_length=500, verbose_name="Nombre")
    estado = models.BooleanField(default=True, verbose_name='Estado')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Creado por')
    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.CASCADE,
        verbose_name='Centro de costo'
    )
    medida = models.ForeignKey(MedidaActividad, on_delete=models.CASCADE, verbose_name='Medida')
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Grupo')
    
    def __str__(self):
        return f"{self.codigo}, {self.name}"
    
class MedidaTarea(models.Model):
    name = models.CharField(max_length=500, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"   
     
class Tarea(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    name = models.CharField(max_length=500, verbose_name="Nombre")
    trazabilidad = models.CharField(max_length=2, choices=TRAZABILIDAD_CHOICES, verbose_name="Trazabilidad")
    medida = models.ForeignKey(MedidaTarea, on_delete=models.CASCADE, verbose_name='Medida')
    criterio = models.TextField(verbose_name="Criterio", null=True, blank=True)
    definicion = models.TextField(verbose_name="Definicion", null=True, blank=True)

    def __str__(self):
        return f"{self.actividad}, {self.name}"

class ReporteTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, verbose_name='Tarea', related_name='report_tarea')
    year = models.PositiveIntegerField(verbose_name='Año')
    mes = models.CharField(max_length=20, verbose_name="Mes")  
    prog_fisica = models.IntegerField(verbose_name='Prog. Física', default=0, null=True, blank=True)
    repro_fisica = models.IntegerField(verbose_name='Repro. Física', default=0, null=True, blank=True)
    ejec_fisica = models.IntegerField(verbose_name='Ejec. Física', default=0, null=True, blank=True)
    comentario = models.CharField(max_length=500,verbose_name='Comentario', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Se asegura de que este campo se agregue automáticamente
    sustento = models.CharField(max_length=500, blank=True, null=True)
    alerta = models.TextField(verbose_name='Alerta', blank=True, null=True)  # De CharField a TextField
    recomendaciones = models.TextField(verbose_name='Recomendaciones', blank=True, null=True)  # De CharField a TextField
    campos_bloqueados = models.BooleanField(default=False, verbose_name="Campos Bloqueados")
    dias_adicionales = models.PositiveIntegerField(default=0)
       
    def __str__(self):
        return f"{self.tarea} - {self.year} - {self.mes}"
    
class ReporteActividad(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name='Actividad', related_name='report_actividad')
    year = models.PositiveIntegerField(verbose_name='Año')
    mes = models.CharField(max_length=20, verbose_name="Mes")  
    prog_ppto = models.DecimalField(verbose_name='Prog. Presupuestal', max_digits=15, decimal_places=2, null=True, blank=True)
    prog_5_21 = models.DecimalField(verbose_name='Prog. Gen. 5.21', max_digits=15, decimal_places=2, null=True, blank=True)
    prog_5_23 = models.DecimalField(verbose_name='Prog. Gen. 5.23', max_digits=15, decimal_places=2, null=True, blank=True)
    prog_5_26 = models.DecimalField(verbose_name='Prog. Gen. 5.26', max_digits=15, decimal_places=2, null=True, blank=True)
    repro_ppto = models.DecimalField(verbose_name='Act. Presupuestal', max_digits=15, decimal_places=2, null=True, blank=True)
    act_5_21 = models.DecimalField(verbose_name='Act. Gen. 5.21', max_digits=15, decimal_places=2, null=True, blank=True)
    act_5_23 = models.DecimalField(verbose_name='Act. Gen. 5.23', max_digits=15, decimal_places=2, null=True, blank=True)
    act_5_26 = models.DecimalField(verbose_name='Act. Gen. 5.26', max_digits=15, decimal_places=2, null=True, blank=True)
    
    ejec_ppto = models.DecimalField(verbose_name='Ejec. Presupuestal', max_digits=15, decimal_places=2, null=True, blank=True)
    ejec_5_21 = models.DecimalField(verbose_name='Ejec. Gen. 5.21', max_digits=15, decimal_places=2, null=True, blank=True)
    ejec_5_23 = models.DecimalField(verbose_name='Ejec. Gen. 5.23', max_digits=15, decimal_places=2, null=True, blank=True)
    ejec_5_26 = models.DecimalField(verbose_name='Ejec. Gen. 5.26', max_digits=15, decimal_places=2, null=True, blank=True)
    campos_bloqueados = models.BooleanField(default=False, verbose_name="Campos Bloqueados")
    
    def __str__(self):
        return f"{self.actividad} - {self.year} - {self.mes}"    
    
class Archivo(models.Model):
    reporte_tarea = models.ForeignKey(ReporteTarea, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='files/', null=True, blank=True, verbose_name="Archivo")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name
