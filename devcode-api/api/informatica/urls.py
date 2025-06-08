# api/personal/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from api.informatica.views import *

router = DefaultRouter()

router.register(r'all', InformaticaViewSet)

urlpatterns = router.urls
