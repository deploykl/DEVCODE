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

from api.patrimonio.serializers import *
from api.patrimonio.models import *

@extend_schema_view(
    list = extend_schema(description = "Permite obtener una lista de tarea"),
    retrieve = extend_schema(description = "Permite obtener una tarea"),
    create = extend_schema(description = "Permite crear una tarea"),
    update = extend_schema(description = "Permite actualizar una tarea"),
    destroy = extend_schema(description = "Permite eliminar una tarea"),
    
)
class PatrimonioViewSet(viewsets.ModelViewSet):
    queryset = Patrimonio.objects.all()
    serializer_class = PatrimonioSerializer
    permission_classes = [IsSuperUser]  # Permitir acceso solo a superusuarios
    ordering = ['id']
    ordering_fields = '__all__'