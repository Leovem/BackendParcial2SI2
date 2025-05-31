from django.urls import path
from .views import CursoViewSet, InscripcionViewSet, MateriaViewSet, CursoMateriaViewSet

urlpatterns = [
    path('cursos/', CursoViewSet.as_view({'get': 'list', 'post': 'create'}), name='curso-list'),
    path('cursos/<int:pk>/', CursoViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='curso-detail'),
    path('cursos/<int:pk>/planilla/', CursoViewSet.as_view({'get': 'planilla'}), name='curso-planilla'),


    path('inscripciones/', InscripcionViewSet.as_view({'get': 'list', 'post': 'create'}), name='inscripcion-list'),
    path('inscripciones/<int:pk>/', InscripcionViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='inscripcion-detail'),

    path('materias/', MateriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='materia-list'),
    path('materias/<int:pk>/', MateriaViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='materia-detail'),

    path('curso-materias/', CursoMateriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='cursomateria-list'),
    path('curso-materias/<int:pk>/', CursoMateriaViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='cursomateria-detail'),

]
