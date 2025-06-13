from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PrediccionML, RecomendacionIA
from .serializers import PrediccionMLSerializer, RecomendacionIASerializer
from authapp.models import Estudiante
from authapp.serializers import EstudianteSerializer

class PrediccionMLViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrediccionML.objects.all()
    serializer_class = PrediccionMLSerializer

class RecomendacionIAViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecomendacionIA.objects.all()
    serializer_class = RecomendacionIASerializer







class RendimientoIAViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def por_estudiante(self, request):
        estudiante_id = request.query_params.get("estudiante_id")
        if not estudiante_id:
            return Response({"error": "Falta el parámetro estudiante_id"}, status=400)

        try:
            estudiante = Estudiante.objects.select_related('persona').get(id=estudiante_id)
        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"}, status=404)

        predicciones = PrediccionML.objects.filter(estudiante_id=estudiante_id).order_by('-fecha_prediccion')
        recomendaciones = RecomendacionIA.objects.filter(estudiante_id=estudiante_id)

        data_pred = [{
            "gestion_id": p.gestion_id,
            "bimestre_id": p.bimestre_id,
            "puntaje_predicho": p.puntaje_predicho,
            "probabilidad_riesgo": p.probabilidad_riesgo,
            "fecha_prediccion": p.fecha_prediccion
        } for p in predicciones]

        data_rec = [{
            "gestion_id": r.gestion_id,
            "bimestre_id": r.bimestre_id,
            "recomendaciones": r.recomendaciones  # ← aquí está el cambio clave
        } for r in recomendaciones]

        return Response({
            "estudiante": {
                "id": estudiante.id,
                "nombre": f"{estudiante.persona.nombres} {estudiante.persona.apellidos}"
            },
            "predicciones": data_pred,
            "recomendaciones": data_rec
        })
