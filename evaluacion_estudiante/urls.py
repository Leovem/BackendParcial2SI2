from django.urls import path
from .views import RegistrarCalificacionView, RegistrarParticipacionView, RegistrarAsistenciaView

urlpatterns = [
    path('registrar-calificacion/', RegistrarCalificacionView.as_view(), name='registrar-calificacion'),
    path('registrar-participacion/', RegistrarParticipacionView.as_view(), name='registrar-participacion'),
    path('registrar-asistencia/', RegistrarAsistenciaView.as_view(), name='registrar-asistencia'),
]
