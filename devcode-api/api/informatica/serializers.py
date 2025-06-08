from api.informatica.models import *
from rest_framework import serializers

class InformaticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informatica
        fields = "__all__" #obtener todos los campos