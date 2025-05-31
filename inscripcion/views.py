from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
#from estructura_academica.models import Bimestre
from .models import Curso, Inscripcion, Materia, CursoMateria, HorarioClase
from .serializers import CursoSerializer, InscripcionSerializer, MateriaSerializer, CursoMateriaSerializer, HorarioClaseSerializer


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

    @action(detail=True, methods=['get'], url_path='estudiantes')
    def estudiantes_por_curso(self, request, pk=None):
        curso = self.get_object()
        gestion_id = request.query_params.get('gestion_id')

        if not gestion_id:
            return Response({'error': 'Debe proporcionar gestion_id como query param.'}, status=400)

        if str(curso.gestion.id) != gestion_id:
            return Response({'error': 'El curso no pertenece a la gestión indicada.'}, status=400)

        inscripciones = Inscripcion.objects.filter(
            curso=curso, gestion_id=gestion_id
        ).select_related('estudiante__persona')

        estudiantes = []
        for insc in inscripciones:
            persona = insc.estudiante.persona
            estudiantes.append({
                'id': insc.estudiante.id,
                'nombre_completo': f'{persona.nombres} {persona.apellidos}',
                'ci': persona.ci,
                'fecha_inscripcion': insc.fecha_inscripcion
            })

        return Response({
            'curso': {
                'id': curso.id,
                'nombre': f'{curso.grado.nombre}{curso.paralelo}',
                'grado': curso.grado.nombre,
                'paralelo': curso.paralelo,
                'gestion': curso.gestion.anio
            },
            'estudiantes': estudiantes
        })
    
    @action(detail=True, methods=['get'], url_path='horario')
    def horario(self, request, pk=None):
        curso = self.get_object()
        gestion_id = request.query_params.get('gestion_id')

        if not gestion_id:
            return Response({'error': 'Debe proporcionar gestion_id como query param.'}, status=400)

        if str(curso.gestion.id) != gestion_id:
            return Response({'error': 'El curso no pertenece a la gestión indicada.'}, status=400)

        horarios = HorarioClase.objects.filter(
            curso_materia__curso=curso
        ).select_related('curso_materia__materia', 'curso_materia__docente__persona')

        datos = []
        for h in horarios:
            cm = h.curso_materia
            docente = cm.docente
            persona = getattr(docente, 'persona', None)
            datos.append({
                'dia_semana': h.dia_semana,
                'hora_inicio': h.hora_inicio.strftime('%H:%M'),
                'hora_fin': h.hora_fin.strftime('%H:%M'),
                'materia': cm.materia.nombre,
                'docente': f'{persona.nombres} {persona.apellidos}' if persona else '',
                'aula': h.aula
            })

        return Response({
            'curso': {
                'id': curso.id,
                'nombre': f'{curso.grado.nombre}{curso.paralelo}',
                'gestion': curso.gestion.anio
            },
            'horario': sorted(datos, key=lambda x: (x['dia_semana'], x['hora_inicio']))
        })


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class CursoMateriaViewSet(viewsets.ModelViewSet):
    queryset = CursoMateria.objects.all()
    serializer_class = CursoMateriaSerializer

class HorarioClaseViewSet(viewsets.ModelViewSet):
    queryset = HorarioClase.objects.all()
    serializer_class = HorarioClaseSerializer

