from django.urls import path
from .views import (
    ListarEstudiantesView,
    ListarDocentesView,
    ListarPadresView,
    EditarEstudianteView,
    EditarDocenteView, 
    EditarPadreFamiliaView,
    EditarUsuarioView,
    HijosDePadreView,
    CrearRelacionEstudiantePadreView
)

urlpatterns = [
    path('estudiantes/', ListarEstudiantesView.as_view(), name='listar-estudiantes'),
    path('docentes/', ListarDocentesView.as_view(), name='listar-docentes'),
    path('padres/', ListarPadresView.as_view(), name='listar-padres'),
    path('estudiantes/<int:pk>/editar/', EditarEstudianteView.as_view(), name='editar-estudiante'),
    path('docentes/<int:pk>/editar/', EditarDocenteView.as_view(), name='editar-docente'),
    path('padres/<int:pk>/editar/', EditarPadreFamiliaView.as_view(), name='editar-padre'),
    path('usuarios/<int:pk>/editar/', EditarUsuarioView.as_view(), name='editar_usuario'),
    path('padre/<int:padre_id>/hijos/', HijosDePadreView.as_view(), name='hijos-de-padre'),
    path('relacion-estudiante-padre/', CrearRelacionEstudiantePadreView.as_view(), name='crear-relacion'),
]
