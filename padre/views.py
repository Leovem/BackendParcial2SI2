from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from authapp.models import EstudiantePadre
from evaluacion_estudiante.models import Calificacion, Asistencia, Participacion
from evaluacion_estudiante.serializers import CalificacionSerializer, AsistenciaSerializer, ParticipacionSerializer
from authapp.serializers import EstudianteSerializer
from evaluacion_estudiante.utils import obtener_ultima_gestion


def obtener_padre(request):
    try:
        return request.user.persona.padrefamilia
    except:
        raise NotFound("El usuario no tiene un perfil de padre de familia.")


class HijosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        padre = obtener_padre(request)
        relaciones = EstudiantePadre.objects.filter(padre=padre).select_related('estudiante')
        estudiantes = [r.estudiante for r in relaciones]
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)


class NotasHijoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, estudiante_id):
        padre = obtener_padre(request)
        if not EstudiantePadre.objects.filter(padre=padre, estudiante_id=estudiante_id).exists():
            raise NotFound("Este estudiante no está asignado a usted.")

        gestion = obtener_ultima_gestion()
        calificaciones = Calificacion.objects.filter(estudiante_id=estudiante_id, curso__gestion=gestion)
        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)


class AsistenciaHijoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, estudiante_id):
        padre = obtener_padre(request)
        if not EstudiantePadre.objects.filter(padre=padre, estudiante_id=estudiante_id).exists():
            raise NotFound("Este estudiante no está asignado a usted.")

        gestion = obtener_ultima_gestion()
        asistencias = Asistencia.objects.filter(estudiante_id=estudiante_id, curso__gestion=gestion)
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)


class ParticipacionHijoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, estudiante_id):
        padre = obtener_padre(request)
        if not EstudiantePadre.objects.filter(padre=padre, estudiante_id=estudiante_id).exists():
            raise NotFound("Este estudiante no está asignado a usted.")

        gestion = obtener_ultima_gestion()
        participaciones = Participacion.objects.filter(estudiante_id=estudiante_id, curso__gestion=gestion)
        serializer = ParticipacionSerializer(participaciones, many=True)
        return Response(serializer.data)
