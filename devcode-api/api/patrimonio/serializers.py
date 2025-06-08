from api.patrimonio.models import *
from rest_framework import serializers

class PatrimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrimonio
        fields = "__all__" #obtener todos los campos