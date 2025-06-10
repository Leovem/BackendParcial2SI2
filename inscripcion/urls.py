from django.urls import path
from .views import (
    CursoViewSet,
    InscripcionViewSet,
    MateriaViewSet,
    CursoMateriaViewSet,
    HorarioClaseViewSet
)

urlpatterns = [
    # Cursos
    path('cursos/', CursoViewSet.as_view({'get': 'list', 'post': 'create'}), name='curso-list'),
    path('cursos/<int:pk>/', CursoViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='curso-detail'),
    path('cursos/<int:pk>/planilla/', CursoViewSet.as_view({'get': 'planilla'}), name='curso-planilla'),
    path('cursos/<int:pk>/estudiantes/', CursoViewSet.as_view({'get': 'estudiantes_por_curso'}), name='curso-estudiantes'),
    path('cursos/<int:pk>/horario/', CursoViewSet.as_view({'get': 'horario'}), name='curso-horario'),

    # Inscripciones
    path('inscripciones/', InscripcionViewSet.as_view({'get': 'list', 'post': 'create'}), name='inscripcion-list'),
    path('inscripciones/<int:pk>/', InscripcionViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='inscripcion-detail'),
    path('inscripciones/por-curso/<int:curso_id>/', InscripcionViewSet.as_view({'get': 'por_curso'}), name='inscripciones-por-curso'),

    # Materias
    path('materias/', MateriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='materia-list'),
    path('materias/<int:pk>/', MateriaViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='materia-detail'),

    # Curso-Materias
    path('curso-materias/', CursoMateriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='cursomateria-list'),
    path('curso-materias/<int:pk>/', CursoMateriaViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='cursomateria-detail'),

    # Horarios
    path('horarios/', HorarioClaseViewSet.as_view({'get': 'list', 'post': 'create'}), name='horario-list'),
    path('horarios/<int:pk>/', HorarioClaseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='horario-detail'),
]
