from rest_framework import serializers
from .models import Calificacion, Participacion, Asistencia

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'

    def validate_nota(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("La nota debe estar entre 0 y 100.")
        return value



class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

    def validate_estado(self, value):
        estados_validos = ['presente', 'ausente', 'tardanza', 'justificado']
        if value not in estados_validos:
            raise serializers.ValidationError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}.")
        return value


class ParticipacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields = '__all__'

    def validate_puntaje(self, value):
        if value < 0:
            raise serializers.ValidationError("El puntaje no puede ser negativo.")
        return value
