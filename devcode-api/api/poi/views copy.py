from django.shortcuts import render
from django.db.models import Count
from datetime import datetime

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, extend_schema_view  # type: ignore
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from api.poi.serializers import *
from api.poi.models import *

class ReporteTareaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
@extend_schema_view(
    list=extend_schema(description="Permite obtener una lista de tarea"),
    retrieve=extend_schema(description="Permite obtener una tarea"),
    create=extend_schema(description="Permite crear una tarea"),
    update=extend_schema(description="Permite actualizar una tarea"),
    destroy=extend_schema(description="Permite eliminar una tarea"),
)
class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    # eliminar multiple
    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No se proporcionaron IDs para eliminar."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtrar actividades con los IDs proporcionados
        actividades = Actividad.objects.filter(id__in=ids)

        # Eliminar las actividades
        count, _ = actividades.delete()

        return Response({"status": "success", "deleted_count": count})

    def perform_create(self, serializer):
        try:
            # Guardar la actividad con el usuario actual
            actividad = serializer.save(user=self.request.user)

            # Crear los reportes de actividad para la nueva actividad
            self.crear_reportes_faltantes(actividad)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def crear_reportes_faltantes(self, actividad):
        year = datetime.now().year
        meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]

        print(
            f"Creando reportes faltantes para la actividad {actividad.id} del año {year}"
        )

        for mes in meses:
            if not ReporteActividad.objects.filter(
                actividad=actividad, year=year, mes=mes
            ).exists():
                print(
                    f"Creando registro para {mes} del año {year} para la actividad {actividad.id}"
                )
                ReporteActividad.objects.create(actividad=actividad, year=year, mes=mes)
            else:
                print(
                    f"El registro para {mes} del año {year} ya existe para la actividad {actividad.id}"
                )

    # Acción personalizada para crear reportes faltantes
    @action(detail=True, methods=["post"], url_path="crear-reportes-faltantes")
    def crear_reportes_faltantes_action(self, request, pk=None):
        """
        Acción personalizada para crear reportes faltantes.
        """
        actividad = get_object_or_404(Actividad, pk=pk)
        year = datetime.now().year
        meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]
        for mes in meses:
            if not ReporteActividad.objects.filter(
                actividad=actividad, year=year, mes=mes
            ).exists():
                ReporteActividad.objects.create(actividad=actividad, year=year, mes=mes)

        return Response(
            {"message": "Reportes faltantes creados o ya existen."},
            status=status.HTTP_200_OK,
        )

    def get_queryset(self):
        user = self.request.user
    
        if user.is_superuser:
            return Actividad.objects.all()
    
        if user.acceso_poi and user.dependencia:
            # Mostrar solo actividades de la misma dependencia que el usuario
            return Actividad.objects.filter(dependencia=user.dependencia)
    
        # Usuario sin permisos o sin dependencia
        return Actividad.objects.none()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.get_queryset()

        # Obtener filtros aplicados
        dependencia_filter = request.query_params.get("dependencia")
        tarea_filter = request.query_params.get("tarea")

        # Filtrar actividades por dependencia y tarea si se proporcionan
        if dependencia_filter:
            queryset = queryset.filter(dependencia__name__icontains=dependencia_filter)

        if tarea_filter:
            tareas_filtradas = Tarea.objects.filter(
                nombre__icontains=tarea_filter, actividad__in=queryset
            )
            queryset = queryset.filter(tarea__in=tareas_filtradas)
            # Obtener los datos de actividad

        dependencia_counts = queryset.values("dependencia__name").annotate(
            count=Count("id")
        )

        # Obtener los datos de tarea
        tarea_counts = (
            Tarea.objects.filter(actividad__in=queryset)
            .values("actividad__dependencia__name")
            .annotate(count=Count("id"))
        )

        # Obtener las IDs de las actividades del queryset
        actividad_ids = queryset.values_list("id", flat=True)
        # Sumar los valores por dependencia

        SUMA_FISICA = (
            ReporteTarea.objects.filter(
                tarea__trazabilidad="SI",  # Filtra por trazabilidad 'SI'
                tarea__actividad__id__in=actividad_ids,  # Filtra solo por las actividades del usuario
            )
            .values("tarea__actividad__dependencia__name")
            .annotate(
                total_prog_fisica=Sum("prog_fisica"),
                total_repro_fisica=Sum("repro_fisica"),
                total_ejec_fisica=Sum(
                    "ejec_fisica"
                ),  # Incluye todos los campos que necesitas sumar
            )
        )

        # Sumar los valores presupuestales por dependencia
        SUMA_PRESUPUESTO = (
            ReporteActividad.objects.filter(actividad__in=queryset)
            .values("actividad__dependencia__name")
            .annotate(
                total_prog_ppto=Sum("prog_ppto"),
                total_repro_ppto=Sum("repro_ppto"),
                total_ejec_ppto=Sum("ejec_ppto"),
            )
        )

        # Convertir los datos a diccionario
        dependencia_counts_dict = {
            item["dependencia__name"]: item["count"] for item in dependencia_counts
        }
        tarea_counts_dict = {
            item["actividad__dependencia__name"]: item["count"] for item in tarea_counts
        }

        SUM_TAREA_REPORT_dict = {
            item["tarea__actividad__dependencia__name"]: {
                "total_prog_fisica": item.get("total_prog_fisica", 0),
                "total_repro_fisica": item.get("total_repro_fisica", 0),
                "total_ejec_fisica": item.get(
                    "total_ejec_fisica", 0
                ),  # Asegúrate de incluir esto
            }
            for item in SUMA_FISICA
        }

        # Convertir los datos a diccionario
        SUM_ACTIVIDAD_REPORT_dict = {
            item["actividad__dependencia__name"]: {
                "total_prog_ppto": item.get("total_prog_ppto", 0),
                "total_repro_ppto": item.get("total_repro_ppto", 0),
                "total_ejec_ppto": item.get("total_ejec_ppto", 0),
            }
            for item in SUMA_PRESUPUESTO
        }

        data = {
            "activities": response.data,
            "dependencia_counts": dependencia_counts_dict,
            "tarea_counts": tarea_counts_dict,
            "SUM_TAREA_REPORT": SUM_TAREA_REPORT_dict,
            "SUM_ACTIVIDAD_REPORT": SUM_ACTIVIDAD_REPORT_dict,
        }
        return Response(data)


class MedidaActividadViewSet(viewsets.ModelViewSet):
    queryset = MedidaActividad.objects.all()
    serializer_class = MedidaActividadSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    # eliminar multiple
    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No se proporcionaron IDs para eliminar."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtrar actividades con los IDs proporcionados
        medidas = MedidaActividad.objects.filter(id__in=ids)

        # Eliminar las actividades
        count, _ = medidas.delete()

        return Response({"status": "success", "deleted_count": count})


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        queryset = Tarea.objects.all()
        actividad_id = self.request.query_params.get("actividad")
        if actividad_id:
            queryset = queryset.filter(actividad_id=actividad_id)
        return queryset

    def perform_create(self, serializer):
        tarea = serializer.save()
        print(f"Tarea creada: {tarea.id}")
        self.crear_registros_faltantes(tarea.id)

    def crear_registros_faltantes(self, tarea_id):
        tarea = get_object_or_404(Tarea, id=tarea_id)
        year = datetime.now().year
        meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]

        print(f"Creando registros faltantes para la tarea {tarea_id} del año {year}")

        for mes in meses:
            if not ReporteTarea.objects.filter(
                tarea=tarea, year=year, mes=mes
            ).exists():
                print(
                    f"Creando registro para {mes} del año {year} para la tarea {tarea_id}"
                )
                ReporteTarea.objects.create(tarea=tarea, year=year, mes=mes)
            else:
                print(
                    f"El registro para {mes} del año {year} ya existe para la tarea {tarea_id}"
                )

        # Nueva acción personalizada

    @action(detail=True, methods=["post"], url_path="crear-reportes-faltantes")
    def crear_reportes_faltantes(self, request, pk=None):
        """
        Acción personalizada para crear reportes faltantes.
        """
        tarea = get_object_or_404(Tarea, pk=pk)
        year = datetime.now().year
        meses = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]

        for mes in meses:
            if not ReporteTarea.objects.filter(
                tarea=tarea, year=year, mes=mes
            ).exists():
                ReporteTarea.objects.create(tarea=tarea, year=year, mes=mes)

        return Response(
            {"message": "Reportes faltantes creados o ya existen."}, status=200
        )


class MedidaTareaViewSet(viewsets.ModelViewSet):
    queryset = MedidaTarea.objects.all()
    serializer_class = MedidaTareaSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)


class ReporteTareaViewSet(viewsets.ModelViewSet):
    queryset = ReporteTarea.objects.all()
    serializer_class = ReporteTareaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        'year': ['exact'],
        'mes': ['exact', 'iexact'],
        'tarea__id': ['exact'],
    }
    ordering_fields = ['year', 'mes', 'tarea__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Obtener parámetros de consulta
        year = self.request.query_params.get('year')
        mes = self.request.query_params.get('mes')
        tarea_id = self.request.query_params.get('tarea_id')
        
        # Aplicar filtros
        if year:
            queryset = queryset.filter(year=year)
        if mes:
            queryset = queryset.filter(mes__iexact=mes)
        if tarea_id:
            queryset = queryset.filter(tarea_id=tarea_id)
            
        return queryset.select_related('tarea', 'tarea__actividad')

    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request):
        ids = request.data.get('ids', [])
        campos_bloqueados = request.data.get('campos_bloqueados', None)
        
        if not ids or campos_bloqueados is None:
            return Response(
                {'error': 'IDs and campos_bloqueados are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Update all reports with the given IDs
        updated = ReporteTarea.objects.filter(id__in=ids).update(
            campos_bloqueados=campos_bloqueados
        )
        
        return Response({
            'status': 'success',
            'updated_count': updated
        })
           
    @action(detail=False, methods=['get'])
    def resumen(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Calcular totales
        total_prog = queryset.aggregate(Sum('prog_fisica'))['prog_fisica__sum'] or 0
        total_repro = queryset.aggregate(Sum('repro_fisica'))['repro_fisica__sum'] or 0
        total_ejec = queryset.aggregate(Sum('ejec_fisica'))['ejec_fisica__sum'] or 0
        
        return Response({
            'total_prog_fisica': total_prog,
            'total_repro_fisica': total_repro,
            'total_ejec_fisica': total_ejec,
            'porcentaje_avance': round((total_ejec / total_repro * 100), 2) if total_repro else 0
        })
    
class ReporteActividadViewSet(viewsets.ModelViewSet):
    queryset = ReporteActividad.objects.all()
    serializer_class = ReporteActividadSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    def get_queryset(self):
        queryset = super().get_queryset()
        actividad_id = self.request.query_params.get("actividad", None)
        if actividad_id:
            return queryset.filter(actividad_id=actividad_id)
        return queryset
    
    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request):
          """
          Versión simplificada - solo actualiza campos_bloqueados
          sin validaciones de fecha/mes
          """
          ids = request.data.get('ids', [])
          campos_bloqueados = request.data.get('campos_bloqueados', None)

          if not ids or campos_bloqueados is None:
              return Response(
                  {'error': 'Se requieren IDs y campos_bloqueados'},
                  status=status.HTTP_400_BAD_REQUEST
              )

          # Actualización masiva simple
          updated = ReporteActividad.objects.filter(id__in=ids).update(
              campos_bloqueados=campos_bloqueados
          )

          return Response({
              'status': 'success',
              'updated_count': updated
          })   


class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        file = request.FILES.get("archivo")
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def count(self, request, *args, **kwargs):
        tarea_id = request.query_params.get("tarea")
        mes = request.query_params.get("mes")

        # Filtrar ReporteTarea según tarea_id y mes
        reportes = ReporteTarea.objects.all()
        if tarea_id:
            reportes = reportes.filter(id=tarea_id)
        if mes:
            reportes = reportes.filter(mes=mes)

        # Contar archivos asociados a los reportes filtrados
        total_archivos = Archivo.objects.filter(reporte_tarea__in=reportes).count()

        return Response({"total_archivos": total_archivos}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        tarea_id = request.query_params.get("tarea")
        mes = request.query_params.get("mes")

        # Obtener todos los ReporteTarea para el mes y tarea especificados
        reportes = ReporteTarea.objects.all()
        if tarea_id:
            reportes = reportes.filter(id=tarea_id)
        if mes:
            reportes = reportes.filter(mes=mes)

        # Obtener archivos correspondientes a los reportes filtrados
        archivos = Archivo.objects.filter(reporte_tarea__in=reportes)

        serializer = self.get_serializer(archivos, many=True)
        return Response(serializer.data)
