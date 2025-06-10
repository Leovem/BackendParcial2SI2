from django.urls import path
from .views import (
    NivelViewSet,
    GradoViewSet,
    GestionAcademicaViewSet,
    BimestreViewSet,
    BimestresPorAnioView,
    UltimaGestionView,

)

urlpatterns = [
    # Nivel
    path('niveles/', NivelViewSet.as_view({'get': 'list', 'post': 'create'}), name='nivel-list'),
    path('niveles/<int:pk>/', NivelViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='nivel-detail'),

    # Grado
    path('grados/', GradoViewSet.as_view({'get': 'list', 'post': 'create'}), name='grado-list'),
    path('grados/<int:pk>/', GradoViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='grado-detail'),
    path('grados/por-nivel/<int:nivel_id>/', GradoViewSet.as_view({'get': 'por_nivel'}), name='grados-por-nivel'),


    # Gestión Académica
    path('gestiones/', GestionAcademicaViewSet.as_view({'get': 'list', 'post': 'create'}), name='gestion-list'),
    path('gestiones/<int:pk>/', GestionAcademicaViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='gestion-detail'),
    path('gestiones/ultima/', UltimaGestionView.as_view(), name='gestion-ultima'),


    # Bimestre
    path('bimestres/', BimestreViewSet.as_view({'get': 'list', 'post': 'create'}), name='bimestre-list'),
    path('bimestres/<int:pk>/', BimestreViewSet.as_view({'put': 'update', 'get': 'retrieve'}), name='bimestre-detail'),
    path('bimestres-por-anio/<int:anio>/', BimestresPorAnioView.as_view(), name='bimestres-por-anio'),
]
