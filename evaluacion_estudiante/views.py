from rest_framework import viewsets
from .models import Calificacion, Participacion, Asistencia
from .serializers import CalificacionSerializer, ParticipacionSerializer, AsistenciaSerializer
from .utils import obtener_ultima_gestion


class CalificacionViewSet(viewsets.ModelViewSet):
    serializer_class = CalificacionSerializer

    def get_queryset(self):
        return Calificacion.objects.filter(
            curso__gestion=obtener_ultima_gestion()
        )


class ParticipacionViewSet(viewsets.ModelViewSet):
    serializer_class = ParticipacionSerializer

    def get_queryset(self):
        return Participacion.objects.filter(
            curso__gestion=obtener_ultima_gestion()
        )


class AsistenciaViewSet(viewsets.ModelViewSet):
    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        return Asistencia.objects.filter(
            curso__gestion=obtener_ultima_gestion()
        )
