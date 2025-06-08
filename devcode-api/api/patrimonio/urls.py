# api/personal/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from api.patrimonio.views import *

router = DefaultRouter()

router.register(r'all', PatrimonioViewSet)

urlpatterns = router.urls
