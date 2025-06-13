from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import CursoMateriaDetalleSerializer

from inscripcion.models import CursoMateria, Inscripcion
from evaluacion_estudiante.models import Asistencia, Calificacion
from authapp.serializers import EstudianteSerializer
from inscripcion.serializers import CursoMateriaSerializer
from evaluacion_estudiante.serializers import AsistenciaSerializer, CalificacionSerializer
from .utils import obtener_ultima_gestion


class MisCursosView(APIView):
    def get(self, request):
        docente_id = request.query_params.get("docente_id")
        if not docente_id:
            return Response({"error": "Falta el parámetro docente_id"}, status=400)

        gestion = obtener_ultima_gestion()

        cursos = CursoMateria.objects.filter(
            docente_id=docente_id,
            curso__gestion=gestion
        )
        serializer = CursoMateriaDetalleSerializer(cursos, many=True)
        return Response(serializer.data)


class EstudiantesPorCursoView(APIView):
    def get(self, request, curso_id):
        gestion = obtener_ultima_gestion()
        inscripciones = Inscripcion.objects.filter(
            curso_id=curso_id,
            gestion=gestion
        ).select_related('estudiante__persona')

        estudiantes = [i.estudiante for i in inscripciones]
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)


class RegistrarAsistenciaView(APIView):
    def post(self, request):
        docente_id = request.data.get("docente_id")
        if not docente_id:
            return Response({"error": "Falta el campo docente_id"}, status=400)

        serializer = AsistenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curso = serializer.validated_data['curso']
        materia = serializer.validated_data['materia']

        if not CursoMateria.objects.filter(curso=curso, materia=materia, docente_id=docente_id).exists():
            raise PermissionDenied("No puedes registrar asistencia en este curso y materia.")

        serializer.save()
        return Response(serializer.data, status=201)


class RegistrarCalificacionView(APIView):
    def post(self, request):
        docente_id = request.data.get("docente_id")
        if not docente_id:
            return Response({"error": "Falta el campo docente_id"}, status=400)

        serializer = CalificacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curso = serializer.validated_data['curso']
        materia = serializer.validated_data['materia']

        if not CursoMateria.objects.filter(curso=curso, materia=materia, docente_id=docente_id).exists():
            raise PermissionDenied("No puedes registrar calificaciones en este curso y materia.")

        serializer.save()
        return Response(serializer.data, status=201)
