from api.poi.models import *
from rest_framework import serializers
from django.db.models import Sum

class ActividadSerializer(serializers.ModelSerializer):
    dependencia_name = serializers.ReadOnlyField(source='dependencia.name')
    medida_name  = serializers.CharField(source='medida.name', read_only=True)
    dependencia_actividad_count = serializers.SerializerMethodField()
    suma_prog_fisica = serializers.SerializerMethodField()
    suma_repro_fisica = serializers.SerializerMethodField()
    suma_ejec_fisica = serializers.SerializerMethodField()
    PorEjecAvance = serializers.SerializerMethodField()
    PROG_PPTO_ANUAL = serializers.SerializerMethodField()  # Nuevo campo
    REPRO_PPTO_ANUAL = serializers.SerializerMethodField()  # Nuevo campo
    EJEC_PPTO_ANUAL = serializers.SerializerMethodField()  # Nuevo campo
    POR_PPTO_AVANCE = serializers.SerializerMethodField()  # Nuevo campo


    class Meta:
        model = Actividad
        fields = ("id", "codigo", "name", "estado",
                  "user", "dependencia_name","medida","medida_name","dependencia", 
                  "dependencia_actividad_count", "suma_prog_fisica",
                  "suma_repro_fisica", "suma_ejec_fisica",
                  "PorEjecAvance", "PROG_PPTO_ANUAL",
                  "REPRO_PPTO_ANUAL", "EJEC_PPTO_ANUAL",
                  "POR_PPTO_AVANCE",
                  )
        
        read_only_fields = ("user",) #para q no solicite enviar desde el front-end


    def get_dependencia_actividad_count(self, obj):
        # Contar el total de actividades por dependencia para la instancia actual
        return Actividad.objects.filter(dependencia=obj.dependencia).count()

    def get_suma_campo(self, obj, campo):
        # Filtra ReporteTarea donde la tarea asociada tenga trazabilidad igual a 'SI'
        queryset = ReporteTarea.objects.filter(
            tarea__actividad=obj,
            tarea__trazabilidad='SI'  # Asegúrate de que 'SI' es el valor correcto
        )
        # Agrega los valores del campo especificado
        total = queryset.aggregate(total=Sum(campo))['total'] or 0
        return total

    def get_suma_prog_fisica(self, obj):
        return self.get_suma_campo(obj, 'prog_fisica')

    def get_suma_repro_fisica(self, obj):
        return self.get_suma_campo(obj, 'repro_fisica')

    def get_suma_ejec_fisica(self, obj):
        return self.get_suma_campo(obj, 'ejec_fisica')

    def get_PorEjecAvance(self, obj):
        total_repro_fisica = self.get_suma_repro_fisica(obj)
        total_ejec_fisica = self.get_suma_ejec_fisica(obj)
        if total_repro_fisica == 0:
            return 0
        return round((total_ejec_fisica / total_repro_fisica) * 100, 2)
    
#======================================PRESUPUESTO======================================
    def get_TotalPPTO(self, obj, campo):
        return ReporteActividad.objects.filter(
            actividad=obj
        ).aggregate(total=Sum(campo))['total'] or 0

    def get_PROG_PPTO_ANUAL(self, obj):
        return self.get_TotalPPTO(obj, 'prog_ppto')

    def get_REPRO_PPTO_ANUAL(self, obj):
        return self.get_TotalPPTO(obj, 'repro_ppto')
        
    def get_EJEC_PPTO_ANUAL(self, obj):
        return self.get_TotalPPTO(obj, 'ejec_ppto')
        
    def get_POR_PPTO_AVANCE(self, obj):
        suma_ejec_ppto = self.get_EJEC_PPTO_ANUAL(obj)
        suma_repro_ppto = self.get_REPRO_PPTO_ANUAL(obj)
        if suma_repro_ppto == 0:
            return 0
        return round((suma_ejec_ppto / suma_repro_ppto) * 100, 2)
    

class MedidaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedidaActividad
        fields = '__all__'   
            
        
class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'   
# =========================== RELACIÓN PARA TAREA =========================  
    
class ReporteTareaSerializer(serializers.ModelSerializer):
    tarea_name = serializers.CharField(source='tarea.name', read_only=True)
    actividad_name = serializers.CharField(source='tarea.actividad.name', read_only=True)
    dependencia_name = serializers.CharField(source='tarea.actividad.dependencia.name', read_only=True)
    
    class Meta:
        model = ReporteTarea
        fields = '__all__'
        extra_kwargs = {
            'fecha_creacion': {'read_only': True},
            'sustento': {'required': False, 'allow_blank': True},
            'alerta': {'required': False, 'allow_blank': True},
            'recomendaciones': {'required': False, 'allow_blank': True}
        }
class ReporteActividadSerializer(serializers.ModelSerializer):
    actividad_name = serializers.CharField(source='actividad.name', read_only=True)  # Agregar este campo

    class Meta:
        model = ReporteActividad
        fields = '__all__'

                                         
class TareaSerializer(serializers.ModelSerializer):
    actividad_name = serializers.ReadOnlyField(source="actividad.name")
    medida_name  = serializers.CharField(source='medida.name', read_only=True)
    actividad_medida_name = serializers.CharField(source='actividad.medida.name', read_only=True)
    mes = ReporteTareaSerializer(many=True, read_only=True, source='report_tarea')
    TotalProgFisica = serializers.SerializerMethodField()
    TotalReproFisica = serializers.SerializerMethodField()
    TotalEjecFisica = serializers.SerializerMethodField()
    PorEjecAvance = serializers.SerializerMethodField()
   
    class Meta:
        model = Tarea
        fields = (
            "id", "name", "trazabilidad", "actividad","medida",
            "medida_name","actividad_name", "definicion","actividad_medida_name", 
            "mes", "criterio", "TotalProgFisica", "TotalReproFisica", 
            "TotalEjecFisica", "PorEjecAvance")
    
    def get_TotalProgFisica(self, obj):
        return sum(reporte.prog_fisica for reporte in obj.report_tarea.all())

    def get_TotalReproFisica(self, obj):
        return sum(reporte.repro_fisica for reporte in obj.report_tarea.all())

    def get_TotalEjecFisica(self, obj):
        return sum(reporte.ejec_fisica for reporte in obj.report_tarea.all())
    
    def get_PorEjecAvance(self, obj):
        total_repro_fisica = self.get_TotalReproFisica(obj)
        total_ejec_fisica = self.get_TotalEjecFisica(obj)
        if total_repro_fisica == 0:
            return 0
        return round((total_ejec_fisica / total_repro_fisica) * 100, 2)  # Calcula el porcentaje y redondea a 2 decimales
# ===========================================================================                 

class MedidaTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedidaTarea
        fields = '__all__'
        
