from django.urls import path
from rest_framework.routers import DefaultRouter
from api.poi.views import *

router = DefaultRouter()

router.register(r'actividad', ActividadViewSet)
router.register(r'medida-actividad', MedidaActividadViewSet)
router.register(r'tarea', TareaViewSet)
router.register(r'medida-tarea', MedidaTareaViewSet)
router.register(r'reporte-tarea', ReporteTareaViewSet)
router.register(r'reporte-actividad', ReporteActividadViewSet)
router.register(r'archivo', ArchivoViewSet)


urlpatterns = router.urls
