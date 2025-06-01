from rest_framework import generics
from .models import Calificacion, Participacion, Asistencia
from .serializers import CalificacionSerializer, ParticipacionSerializer, AsistenciaSerializer

class RegistrarCalificacionView(generics.CreateAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer


class RegistrarParticipacionView(generics.CreateAPIView):
    queryset = Participacion.objects.all()
    serializer_class = ParticipacionSerializer


class RegistrarAsistenciaView(generics.CreateAPIView):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
