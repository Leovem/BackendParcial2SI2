
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
     path('admin/', admin.site.urls),
     path('auth/', include('authapp.urls')),
     path('user/', include('usuarios.urls')),
     path('estructura-academica/', include('estructura_academica.urls')),
     path('inscripcion/', include('inscripcion.urls')),
     path('evaluacion/', include('evaluacion_estudiante.urls')),
     path('alertas/', include('alertas.urls')),
     path('api/ia/', include('ia.urls')),
     path('api/docente/', include('docente.urls')),
     path('api/estudiante/', include('estudiante.urls')),
     path('api/padre/', include('padre.urls')),

]
