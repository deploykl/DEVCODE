from api.dvi.models import *
from rest_framework import serializers

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = "__all__" 
        
class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = "__all__" 
        
class SituacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Situacion
        fields = "__all__" 