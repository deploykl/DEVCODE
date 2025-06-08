#python manage.py shell

#year = datetime.now().year
#meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
#tareas = Tarea.objects.all()
#
#for tarea in tareas:
#    for mes in meses:
#        if not ReporteMensual.objects.filter(tarea=tarea, year=year, mes=mes).exists():
#            print(f"Creando registro para {mes} del año {year} para la tarea {tarea.id}")
#            ReporteMensual.objects.create(tarea=tarea, year=year, mes=mes)
#        else:
#            print(f"El registro para {mes} del año {year} ya existe para la tarea {tarea.id}")


# PARA LA ACTIVIDAD
from datetime import datetime
from api.poi.models import Actividad, ReporteActividad

# Definir el año actual
year = datetime.now().year

# Lista de meses en español
meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

# Obtener todas las actividades
actividades = Actividad.objects.all()

# Crear registros para cada actividad y mes
for actividad in actividades:
    for mes in meses:
        # Verificar si el registro ya existe
        if not ReporteActividad.objects.filter(actividad=actividad, year=year, mes=mes).exists():
            print(f"Creando registro para {mes} del año {year} para la actividad {actividad.id}")
            # Crear el registro
            ReporteActividad.objects.create(actividad=actividad, year=year, mes=mes)
        else:
            print(f"El registro para {mes} del año {year} ya existe para la actividad {actividad.id}")
 