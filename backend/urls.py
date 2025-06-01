
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

]
