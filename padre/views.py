from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from authapp.models import EstudiantePadre
from evaluacion_estudiante.models import Calificacion, Asistencia, Participacion
from evaluacion_estudiante.serializers import CalificacionSerializer, AsistenciaSerializer, ParticipacionSerializer
from authapp.serializers import EstudianteSerializer
from evaluacion_estudiante.utils import obtener_ultima_gestion


class HijosView(APIView):
    def get(self, request):
        padre_id = request.query_params.get("padre_id")
        if not padre_id:
            return Response({"error": "Falta el parámetro padre_id"}, status=400)

        relaciones = EstudiantePadre.objects.filter(padre_id=padre_id).select_related('estudiante__persona')
        estudiantes = [r.estudiante for r in relaciones]
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)


class NotasHijoView(APIView):
    def get(self, request, estudiante_id):
        padre_id = request.query_params.get("padre_id")
        if not padre_id:
            return Response({"error": "Falta el parámetro padre_id"}, status=400)

        if not EstudiantePadre.objects.filter(padre_id=padre_id, estudiante_id=estudiante_id).exists():
            raise NotFound("Este estudiante no está asignado a usted.")

        gestion = obtener_ultima_gestion()
        calificaciones = Calificacion.objects.filter(estudiante_id=estudiante_id, curso__gestion=gestion)
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)


class AsistenciaHijoView(APIView):
    def get(self, request, estudiante_id):
        padre_id = request.query_params.get("padre_id")
        if not padre_id:
            return Response({"error": "Falta el parámetro padre_id"}, status=400)

        if not EstudiantePadre.objects.filter(padre_id=padre_id, estudiante_id=estudiante_id).exists():
            raise NotFound("Este estudiante no está asignado a usted.")

        gestion = obtener_ultima_gestion()
        asistencias = Asistencia.objects.filter(estudiante_id=estudiante_id, curso__gestion=gestion)
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


class ParticipacionHijoView(APIView):
    def get(self, request, estudiante_id):
        padre_id = request.query_params.get("padre_id")
        if not padre_id:
            return Response({"error": "Falta el parámetro padre_id"}, status=400)

        if not EstudiantePadre.objects.filter(padre_id=padre_id, estudiante_id=estudiante_id).exists():
            raise NotFound("Este estudiante no está asignado a usted.")

        gestion = obtener_ultima_gestion()
        participaciones = Participacion.objects.filter(estudiante_id=estudiante_id, curso__gestion=gestion)
        serializer = ParticipacionSerializer(participaciones, many=True)
        return Response(serializer.data)
