import jwt
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.user.serializers import *
from api.user.models import *
from rest_framework.decorators import action
from rest_framework_simplejwt.exceptions import InvalidToken


@extend_schema_view(
    list=extend_schema(description="Permite obtener una lista de tarea"),
    retrieve=extend_schema(description="Permite obtener una tarea"),
    create=extend_schema(description="Permite crear una tarea"),
    update=extend_schema(description="Permite actualizar una tarea"),
    destroy=extend_schema(description="Permite eliminar una tarea"),
)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        # Devuelve solo los detalles del usuario autenticado
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['id']
    ordering_fields = '__all__'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    
    
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crea un objeto RefreshToken a partir del token recibido
            token = RefreshToken(refresh_token)
            # Añade el token a la lista negra
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except InvalidToken:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Las credenciales de autenticación no se proveyeron.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({'detail': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

       # Verificar si el usuario tiene un grupo asociado
        grupo_name = user.groups.first().name if user.groups.exists() else None

        if not grupo_name:
            return Response({'detail': 'El usuario no tiene un grupo asignado. Contacte al administrador.'}, status=status.HTTP_403_FORBIDDEN)

        # Generar tokens si el usuario tiene un grupo válido
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        user_data = {
            'access': access_token,
            'refresh': str(refresh),
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'group': grupo_name,  # Añadir el nombre del grupo
        }

        return Response(user_data, status=status.HTTP_200_OK)


    

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['id']
    ordering_fields = '__all__'
    filter_backends = (DjangoFilterBackend, OrderingFilter)