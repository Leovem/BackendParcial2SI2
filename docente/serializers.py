from rest_framework import serializers
from inscripcion.models import CursoMateria

class CursoMateriaDetalleSerializer(serializers.ModelSerializer):
    nombre_materia = serializers.CharField(source='materia.nombre', read_only=True)
    nombre_curso = serializers.SerializerMethodField()
    gestion = serializers.IntegerField(source='curso.gestion.anio', read_only=True)

    class Meta:
        model = CursoMateria
        fields = ['id', 'curso', 'nombre_curso', 'materia', 'nombre_materia', 'docente', 'gestion']

    def get_nombre_curso(self, obj):
        return f"{obj.curso.grado.nombre}{obj.curso.paralelo}"
