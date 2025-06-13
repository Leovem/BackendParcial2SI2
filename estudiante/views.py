from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from evaluacion_estudiante.models import Calificacion, Asistencia, Participacion
from evaluacion_estudiante.serializers import CalificacionSerializer, AsistenciaSerializer, ParticipacionSerializer
from evaluacion_estudiante.utils import obtener_ultima_gestion


def obtener_estudiante(request):
    try:
        return request.user.persona.estudiante
    except:
        raise NotFound("El usuario no tiene un perfil de estudiante asociado.")


class MisCalificacionesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estudiante = obtener_estudiante(request)
        gestion = obtener_ultima_gestion()
        calificaciones = Calificacion.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)


class MiAsistenciaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estudiante = obtener_estudiante(request)
        gestion = obtener_ultima_gestion()
        asistencias = Asistencia.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


class MiParticipacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        estudiante = obtener_estudiante(request)
        gestion = obtener_ultima_gestion()
        participaciones = Participacion.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        serializer = ParticipacionSerializer(participaciones, many=True)
        return Response(serializer.data)
