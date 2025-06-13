from rest_framework import serializers
from .models import Calificacion, Participacion, Asistencia
from .utils import obtener_ultima_gestion

class CalificacionSerializer(serializers.ModelSerializer):
    materia = serializers.CharField(source='materia.nombre')  # Mostrar nombre de la materia
    curso = serializers.SerializerMethodField()  # Mostrar nombre del curso (opcional)

    class Meta:
        model = Calificacion
        fields = ['id', 'nota', 'observacion', 'fecha_registro', 'estudiante', 'curso', 'materia', 'bimestre']

    def get_curso(self, obj):
        return str(obj.curso)  # Usa el __str__ del modelo Curso

    def validate_nota(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("La nota debe estar entre 0 y 100.")
        return value

    def create(self, validated_data):
        curso = validated_data.get('curso')
        if curso and curso.gestion_id is None:
            curso.gestion_id = obtener_ultima_gestion().id
            curso.save(update_fields=['gestion_id'])
        return super().create(validated_data)



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
