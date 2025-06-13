from django.urls import path
from .views import HijosView, NotasHijoView, AsistenciaHijoView, ParticipacionHijoView

urlpatterns = [
    path('mis-hijos/', HijosView.as_view(), name='padre-mis-hijos'),
    path('hijos/<int:estudiante_id>/notas/', NotasHijoView.as_view(), name='padre-notas-hijo'),
    path('hijos/<int:estudiante_id>/asistencia/', AsistenciaHijoView.as_view(), name='padre-asistencia-hijo'),
    path('hijos/<int:estudiante_id>/participacion/', ParticipacionHijoView.as_view(), name='padre-participacion-hijo'),
]
