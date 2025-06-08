from api.personal.models import *
from rest_framework import serializers
 
class AnexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo
        fields = "__all__" #obtener todos los campos
        
    def validate_name(self, value):
        if value < 0 or value > 9999:
            raise serializers.ValidationError("El número debe estar entre 0 y 9999 (máximo 4 dígitos).")
        return value
       
class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = "__all__" #obtener todos los campos
        
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__" #obtener todos los campos

class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = "__all__" #obtener todos los campos
        
class DependenciaAreaSerializer(serializers.ModelSerializer):
    
    area_name = serializers.ReadOnlyField(source = "area.name")
    dependencia_name = serializers.ReadOnlyField(source = "dependencia.name")

    class Meta:
        model = DependenciaArea
        fields = "__all__" #obtener todos los campos        

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__" #obtener todos los campos
        
class GrupoOcupacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoOcupacional
        fields = "__all__" #obtener todos los campos
        
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = "__all__" #obtener todos los campos
        
class GenericaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generica
        fields = "__all__" #obtener todos los campos