from rest_framework import serializers
from .models import Curso, Inscripcion, Materia, CursoMateria

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class CursoMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoMateria
        fields = '__all__'
