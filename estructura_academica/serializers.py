from rest_framework import serializers
from .models import Nivel, Grado, GestionAcademica, Bimestre

class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = '__all__'

class GestionAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionAcademica
        fields = '__all__'

class BimestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bimestre
        fields = '__all__'
