from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
#from estructura_academica.models import Bimestre
from .mixins import UltimaGestionMixin
from .models import Curso, Inscripcion, Materia, CursoMateria, HorarioClase
from .serializers import CursoSerializer, InscripcionSerializer, MateriaSerializer, CursoMateriaSerializer, HorarioClaseSerializer


class CursoViewSet(UltimaGestionMixin, viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=True, methods=['get'], url_path='planilla')
    def planilla(self, request, pk=None):
        curso = self.get_object()
        gestion_id = self.get_gestion_id(request)

        if str(curso.gestion.id) != str(gestion_id):
            return Response({'error': 'El curso no pertenece a la gestión solicitada.'}, status=400)

        planilla = CursoMateria.objects.filter(
            curso=curso
        ).select_related('materia', 'docente__persona', 'bimestre')

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
        gestion_id = self.get_gestion_id(request)

        if str(curso.gestion.id) != str(gestion_id):
            return Response({'error': 'El curso no pertenece a la gestión indicada.'}, status=400)

        inscripciones = Inscripcion.objects.filter(
            curso=curso, gestion_id=gestion_id
        ).select_related('estudiante__persona')

        estudiantes = [{
            'id': insc.estudiante.id,
            'nombre_completo': f'{insc.estudiante.persona.nombres} {insc.estudiante.persona.apellidos}',
            'ci': insc.estudiante.persona.ci,
            'fecha_inscripcion': insc.fecha_inscripcion
        } for insc in inscripciones]

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
        gestion_id = self.get_gestion_id(request)

        if str(curso.gestion.id) != str(gestion_id):
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



class InscripcionViewSet(UltimaGestionMixin, viewsets.ModelViewSet):
    serializer_class = InscripcionSerializer

    def get_queryset(self):
        gestion_id = self.get_gestion_id(self.request)
        return Inscripcion.objects.filter(gestion_id=gestion_id)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        estudiante_id = data.get('estudiante')
        curso_id = data.get('curso')
        gestion_id = data.get('gestion') or self.get_gestion_id(request)

        existe = Inscripcion.objects.filter(
            estudiante_id=estudiante_id,
            curso_id=curso_id,
            gestion_id=gestion_id
        ).exists()

        if existe:
            return Response({'error': 'Este estudiante ya está inscrito en ese curso para esta gestión.'},
                            status=400)

        data['gestion'] = gestion_id  # forzar la gestión correcta
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
    
    @action(detail=False, methods=['get'], url_path='por-curso/(?P<curso_id>[^/.]+)')
    def por_curso(self, request, curso_id=None):
        gestion_id = self.get_gestion_id(request)
        inscripciones = Inscripcion.objects.filter(curso_id=curso_id, gestion_id=gestion_id).select_related('estudiante__persona')
        data = [{
            'estudiante_id': i.estudiante.id,
            'nombre': f"{i.estudiante.persona.nombres} {i.estudiante.persona.apellidos}",
            'fecha_inscripcion': i.fecha_inscripcion
        } for i in inscripciones]
        return Response(data)




class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class CursoMateriaViewSet(viewsets.ModelViewSet):
    queryset = CursoMateria.objects.all()
    serializer_class = CursoMateriaSerializer

class HorarioClaseViewSet(viewsets.ModelViewSet):
    queryset = HorarioClase.objects.all()
    serializer_class = HorarioClaseSerializer

