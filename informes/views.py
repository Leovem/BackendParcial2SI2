from rest_framework import generics
from .models import ResumenRendimiento
from .serializers import ResumenRendimientoSerializer

class ResumenPorEstudianteView(generics.ListAPIView):
    serializer_class = ResumenRendimientoSerializer

    def get_queryset(self):
        estudiante_id = self.request.query_params.get('estudiante')
        if estudiante_id:
            return ResumenRendimiento.objects.filter(estudiante_id=estudiante_id).order_by('-gestion__anio', 'bimestre__id')
        return ResumenRendimiento.objects.all()
