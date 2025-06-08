from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    dependencia_name = serializers.ReadOnlyField(source="dependencia.name")
    area_name = serializers.ReadOnlyField(source="area.name")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "password2",
            "image",
            "dependencia_name",
            "is_superuser",
            "area_name",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden"}
            )

        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Este nombre de usuario ya está en uso"}
            )

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Este correo electrónico ya está en uso"}
            )

        return data

    def create(self, validated_data):
        validated_data.pop(
            "password2"
        )  # Eliminar la confirmación de contraseña antes de crear el usuario
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UsuarioSerializer(serializers.ModelSerializer):
    condition_name = serializers.ReadOnlyField(
        source="condition.name"
    )  # Leer el nombre de la condición
    area_name = serializers.ReadOnlyField(source="area.name")
    dependencia_name = serializers.ReadOnlyField(source="dependencia.name")
    cargo_name = serializers.ReadOnlyField(source="cargo.name")
    grupo_name = serializers.ReadOnlyField(
        source="grupo.name"
    )  # Leer el nombre del grupo

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "dni",
            "first_name",
            "last_name",
            "condition_name",
            "area_name",
            "dependencia_name",
            "condition",
            "area",
            "email",
            "dependencia",
            "cargo_name",
            "cargo",
            "grupo_name",  # Agregar el campo grupo
            "grupo",  # Asegúrate de incluir este campo para el ID del grupo
            
            "celular",
            "fecha_inicio",
            "fecha_cesado",
            "salario",
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]  # Campos que deseas exponer en la API
