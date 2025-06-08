# api/personal/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from api.dvi.views import *

router = DefaultRouter()

router.register(r'direccion', DireccionViewSet)
router.register(r'meta', MetaViewSet)
router.register(r'situacion', SituacionViewSet)

urlpatterns = router.urls
