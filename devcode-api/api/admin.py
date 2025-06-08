from django.contrib import admin
from api.personal.models import *
from api.user.models import *
from api.poi.models import *
### Register your models here.
##admin.site.register(Task)
admin.site.register(Anexo)
admin.site.register(Condition)
admin.site.register(Area)
admin.site.register(Dependencia)
admin.site.register(Archivo)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('id', 'dependencia', 'codigo', 'name', 'estado', 'user')
    ordering = ('id',)  # Ordenar por id de forma ascendente

admin.site.register(Actividad, ActividadAdmin)

class UserAdmin(admin.ModelAdmin):
    # Define qué campos se mostrarán en la lista de usuarios
    list_display = ('username','first_name', 'email', 'dependencia', 'area')
    
    # Opcional: puedes agregar filtros y campos de búsqueda
    list_filter = ('dependencia', 'area')
    search_fields = ('username', 'first_name', 'email', 'dependencia__name', 'area__name')
    ordering = ('first_name',)

admin.site.register(User, UserAdmin)


#===================    POI ==================
admin.site.register(Grupo)

