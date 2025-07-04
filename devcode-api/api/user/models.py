from django.db import models
from django.contrib.auth.models import AbstractUser 
from api.personal.models import *
from django.contrib.auth.models import Group

from django.db import IntegrityError

# Create your models here.
class User(AbstractUser):  # AbstractUser  heredo data del User
    image = models.ImageField(upload_to='users/%Y/%m/%d',default='img/empty.png', null = True, blank = True)
   
    dni  = models.IntegerField(verbose_name="DNI" , blank=True, null = True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.SET_NULL, null=True, blank=True, related_name='dependencia_users')
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, related_name='area_users')
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, blank=True, related_name='condition_users')   
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_users')   
    profesion = models.ForeignKey(Profesion, on_delete=models.SET_NULL, null=True, blank=True, related_name='prof_users')   
    grupoOcupacional = models.ForeignKey(GrupoOcupacional, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupOcu_users')   
    anexo = models.ForeignKey(Anexo, on_delete=models.SET_NULL, null=True, blank=True, related_name='anexo_users')   
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupo_users')
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupo_estado')
    generica = models.ForeignKey(Generica, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupo_generica')
    
    celular  = models.IntegerField(verbose_name="Celular" , blank=True, null = True)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio", null=True, blank=True)
    fecha_cesado = models.DateField(verbose_name="Fecha de Cese", null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo")
    acceso_poi = models.BooleanField(default=False, verbose_name="Acceso al POI")
    acceso_administracion = models.BooleanField(null=True, blank=True) 
    
# Nuevo campo Género
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Género", null=True, blank=True)

    def delete(self, *args, **kwargs):
        try:
            super(User, self).delete(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error deleting user: {e}")
            
