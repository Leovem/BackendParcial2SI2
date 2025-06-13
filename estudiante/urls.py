from django.urls import path
from .views import MisCalificacionesView, MiAsistenciaView, MiParticipacionView, RendimientoPorCursoView

urlpatterns = [
    path('mis-notas/', MisCalificacionesView.as_view(), name='estudiante-mis-notas'),
    path('mis-notas-curso/', RendimientoPorCursoView.as_view(), name='estudiante-mis-calificaciones'),
    path('mi-asistencia/', MiAsistenciaView.as_view(), name='estudiante-mi-asistencia'),
    path('mi-participacion/', MiParticipacionView.as_view(), name='estudiante-mi-participacion'),

]
