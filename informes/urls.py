from django.urls import path
from .views import ResumenPorEstudianteView

urlpatterns = [
    path('resumen/', ResumenPorEstudianteView.as_view(), name='resumen-por-estudiante'),
]
