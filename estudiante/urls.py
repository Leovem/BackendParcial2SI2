from django.urls import path
from .views import MisCalificacionesView, MiAsistenciaView, MiParticipacionView

urlpatterns = [
    path('mis-notas/', MisCalificacionesView.as_view(), name='estudiante-mis-notas'),
    path('mi-asistencia/', MiAsistenciaView.as_view(), name='estudiante-mi-asistencia'),
    path('mi-participacion/', MiParticipacionView.as_view(), name='estudiante-mi-participacion'),
]
