from django.urls import path
from .views import MisCursosView, EstudiantesPorCursoView, RegistrarAsistenciaView, RegistrarCalificacionView

urlpatterns = [
    path('mis-cursos/', MisCursosView.as_view(), name='docente-mis-cursos'),
    path('cursos/<int:curso_id>/estudiantes/', EstudiantesPorCursoView.as_view(), name='docente-estudiantes-curso'),
    path('asistencia/', RegistrarAsistenciaView.as_view(), name='docente-registrar-asistencia'),
    path('calificacion/', RegistrarCalificacionView.as_view(), name='docente-registrar-calificacion'),
]
