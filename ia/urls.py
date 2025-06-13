from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrediccionMLViewSet, RecomendacionIAViewSet, RendimientoIAViewSet

router = DefaultRouter()
router.register(r'predicciones', PrediccionMLViewSet, basename='prediccionml')
router.register(r'recomendaciones', RecomendacionIAViewSet, basename='recomendacionia')
router.register(r'rendimiento', RendimientoIAViewSet, basename='rendimiento')   # usar este para obtner el rendimiento y recomendacion

urlpatterns = [
    path('', include(router.urls)),
]