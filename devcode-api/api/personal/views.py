from django.shortcuts import render
from api.permissions import IsSuperUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from api.personal.serializers import *
from api.personal.models import *

@extend_schema_view(
    list = extend_schema(description = "Permite obtener una lista de tarea"),
    retrieve = extend_schema(description = "Permite obtener una tarea"),
    create = extend_schema(description = "Permite crear una tarea"),
    update = extend_schema(description = "Permite actualizar una tarea"),
    destroy = extend_schema(description = "Permite eliminar una tarea"),
    
)
class AnexoViewSet(viewsets.ModelViewSet):
    queryset = Anexo.objects.all()
    serializer_class = AnexoSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso solo a superusuarios
    ordering = ['id']
    ordering_fields = '__all__'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)

class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [IsSuperUser]  # Requiere autenticación para acceder
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    
    # Método personalizado para filtrar áreas por dependencia
    @action(detail=False, methods=['get'])
    def filtrar_por_dependencia(self, request):
        dependencia_id = request.query_params.get('dependencia')
        if dependencia_id:
            areas = Area.objects.filter(dependencia_id=dependencia_id)
        else:
            areas = Area.objects.none()
        serializer = self.get_serializer(areas, many=True)
        return Response(serializer.data)
    
class DependenciaAreaViewSet(viewsets.ModelViewSet):
    queryset = DependenciaArea.objects.all()
    serializer_class = DependenciaAreaSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
                
class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class GrupoOcupacionalViewSet(viewsets.ModelViewSet):
    queryset = GrupoOcupacional.objects.all()
    serializer_class = GrupoOcupacionalSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
class GenericaViewSet(viewsets.ModelViewSet):
    queryset = Generica.objects.all()
    serializer_class = GenericaSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso sin autenticación
    ordering = ['id']  # Ordenar por `id` por defecto
    ordering_fields = '__all__'  # Permitir ordenamiento por cualquier campo
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    