from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
#from estructura_academica.models import Bimestre
from .models import Curso, Inscripcion, Materia, CursoMateria
from .serializers import CursoSerializer, InscripcionSerializer, MateriaSerializer, CursoMateriaSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=True, methods=['get'], url_path='planilla')
    def planilla(self, request, pk=None):
        curso = self.get_object()
        gestion_id = request.query_params.get('gestion_id')

        if not gestion_id:
            return Response({'error': 'Debe proporcionar gestion_id como query param.'}, status=400)

        if str(curso.gestion.id) != gestion_id:
            return Response({'error': 'El curso no pertenece a la gestión solicitada.'}, status=400)

        planilla = CursoMateria.objects.filter(
            curso=curso
        ).select_related('materia', 'docente', 'bimestre')

        datos = []
        for cm in planilla:
            docente = cm.docente
            persona = getattr(docente, 'persona', None)
            datos.append({
                'materia': cm.materia.nombre,
                'docente': f'{persona.nombres} {persona.apellidos}' if persona else '',
                'bimestre': cm.bimestre.nombre,
                'gestion': curso.gestion.anio
            })

        return Response(datos)

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class CursoMateriaViewSet(viewsets.ModelViewSet):
    queryset = CursoMateria.objects.all()
    serializer_class = CursoMateriaSerializer


