from django.urls import path
from .views import CalificacionViewSet, ParticipacionViewSet, AsistenciaViewSet

urlpatterns = [
    path('calificaciones/', CalificacionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('participaciones/', ParticipacionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('asistencias/', AsistenciaViewSet.as_view({'get': 'list', 'post': 'create'})),
]
