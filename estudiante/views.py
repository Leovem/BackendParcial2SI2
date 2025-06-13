from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from collections import defaultdict

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


class RendimientoPorCursoView(APIView):
    def get(self, request):
        estudiante_id = request.query_params.get("estudiante_id")
        if not estudiante_id:
            return Response({"error": "Falta el parámetro estudiante_id"}, status=400)

        estudiante = obtener_estudiante_por_id(estudiante_id)
        gestion = obtener_ultima_gestion()

        # Filtrar por gestión activa
        calificaciones = Calificacion.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        asistencias = Asistencia.objects.filter(estudiante=estudiante, curso__gestion=gestion)
        participaciones = Participacion.objects.filter(estudiante=estudiante, curso__gestion=gestion)

        # Agrupar por curso
        datos_por_curso = defaultdict(lambda: {
            "curso_id": None,
            "curso_nombre": "",
            "calificaciones": [],
            "asistencias": [],
            "participaciones": []
        })

        for c in calificaciones:
            curso_id = c.curso.id
            datos = datos_por_curso[curso_id]
            datos["curso_id"] = curso_id
            datos["curso_nombre"] = str(c.curso)
            datos["calificaciones"].append(CalificacionSerializer(c).data)

        for a in asistencias:
            curso_id = a.curso.id
            datos = datos_por_curso[curso_id]
            datos["curso_id"] = curso_id
            datos["curso_nombre"] = str(a.curso)
            datos["asistencias"].append(AsistenciaSerializer(a).data)

        for p in participaciones:
            curso_id = p.curso.id
            datos = datos_por_curso[curso_id]
            datos["curso_id"] = curso_id
            datos["curso_nombre"] = str(p.curso)
            datos["participaciones"].append(ParticipacionSerializer(p).data)

        return Response(list(datos_por_curso.values()))
