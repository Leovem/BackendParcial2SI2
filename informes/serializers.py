from rest_framework import serializers
from .models import ResumenRendimiento

class ResumenRendimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumenRendimiento
        fields = '__all__'
