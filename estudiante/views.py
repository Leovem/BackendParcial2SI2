from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from evaluacion_estudiante.models import Calificacion, Asistencia, Participacion
from evaluacion_estudiante.serializers import CalificacionSerializer, AsistenciaSerializer, ParticipacionSerializer
from evaluacion_estudiante.utils import obtener_ultima_gestion
from authapp.models import Estudiante


def obtener_estudiante_por_id(estudiante_id):
    try:
        return Estudiante.objects.get(id=estudiante_id)
    except Estudiante.DoesNotExist:
        raise NotFound("No se encontró el estudiante con el ID proporcionado.")


class MisCalificacionesView(APIView):
    def get(self, request):
        estudiante_id = request.query_params.get("estudiante_id")
        if not estudiante_id:
            return Response({"error": "Falta el parámetro estudiante_id"}, status=400)

        estudiante = obtener_estudiante_por_id(estudiante_id)
        gestion = obtener_ultima_gestion()

        calificaciones = Calificacion.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)


class MiAsistenciaView(APIView):
    def get(self, request):
        estudiante_id = request.query_params.get("estudiante_id")
        if not estudiante_id:
            return Response({"error": "Falta el parámetro estudiante_id"}, status=400)

        estudiante = obtener_estudiante_por_id(estudiante_id)
        gestion = obtener_ultima_gestion()

        asistencias = Asistencia.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


class MiParticipacionView(APIView):
    def get(self, request):
        estudiante_id = request.query_params.get("estudiante_id")
        if not estudiante_id:
            return Response({"error": "Falta el parámetro estudiante_id"}, status=400)

        estudiante = obtener_estudiante_por_id(estudiante_id)
        gestion = obtener_ultima_gestion()

        participaciones = Participacion.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        serializer = ParticipacionSerializer(participaciones, many=True)
        return Response(serializer.data)
