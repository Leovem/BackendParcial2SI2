from django.urls import path
from .views import (
    NivelViewSet,
    GradoViewSet,
    GestionAcademicaViewSet,
    BimestreViewSet,
)

urlpatterns = [
    # Nivel
    path('niveles/', NivelViewSet.as_view({'get': 'list', 'post': 'create'}), name='nivel-list'),
    path('niveles/<int:pk>/', NivelViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='nivel-detail'),

    # Grado
    path('grados/', GradoViewSet.as_view({'get': 'list', 'post': 'create'}), name='grado-list'),
    path('grados/<int:pk>/', GradoViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='grado-detail'),

    # Gestión Académica
    path('gestiones/', GestionAcademicaViewSet.as_view({'get': 'list', 'post': 'create'}), name='gestion-list'),
    path('gestiones/<int:pk>/', GestionAcademicaViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='gestion-detail'),

    # Bimestre
    path('bimestres/', BimestreViewSet.as_view({'get': 'list', 'post': 'create'}), name='bimestre-list'),
    path('bimestres/<int:pk>/', BimestreViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='bimestre-detail'),
]
