from rest_framework import serializers
from .models import PrediccionML, RecomendacionIA

class PrediccionMLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionML
        fields = '__all__'


class RecomendacionIASerializer(serializers.ModelSerializer):
    class Meta:
        model = RecomendacionIA
        fields = '__all__'
