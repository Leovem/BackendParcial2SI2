from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrediccionMLViewSet, RecomendacionIAViewSet

router = DefaultRouter()
router.register(r'predicciones', PrediccionMLViewSet, basename='prediccionml')
router.register(r'recomendaciones', RecomendacionIAViewSet, basename='recomendacionia')

urlpatterns = [
    path('', include(router.urls)),
]