from api.permissions import IsSuperUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from api.dvi.serializers import *
from api.dvi.models import *

@extend_schema_view(
    list = extend_schema(description = "Permite obtener una lista de tarea"),
    retrieve = extend_schema(description = "Permite obtener una tarea"),
    create = extend_schema(description = "Permite crear una tarea"),
    update = extend_schema(description = "Permite actualizar una tarea"),
    destroy = extend_schema(description = "Permite eliminar una tarea"),
    
)
class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso solo a superusuarios
    ordering = ['id']
    ordering_fields = '__all__'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class MetaViewSet(viewsets.ModelViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso solo a superusuarios
    ordering = ['id']
    ordering_fields = '__all__'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class SituacionViewSet(viewsets.ModelViewSet):
    queryset = Situacion.objects.all()
    serializer_class = SituacionSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso solo a superusuarios
    ordering = ['id']
    ordering_fields = '__all__'
    filter_backends = (DjangoFilterBackend, OrderingFilter)