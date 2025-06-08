# api/personal/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from api.personal.views import *

router = DefaultRouter()

router.register(r'anexo', AnexoViewSet)
router.register(r'condition', ConditionViewSet)
router.register(r'area', AreaViewSet)
router.register(r'dependencia', DependenciaViewSet)
router.register(r'dependencia-area', DependenciaAreaViewSet)
router.register(r'cargo', CargoViewSet)
router.register(r'grupo_ocupacional', GrupoOcupacionalViewSet)
router.register(r'estado', EstadoViewSet)
router.register(r'generica', GenericaViewSet)

urlpatterns = router.urls
