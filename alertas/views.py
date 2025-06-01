from rest_framework import generics
from .models import Alerta
from .serializers import AlertaSerializer

class AlertaListView(generics.ListAPIView):
    serializer_class = AlertaSerializer

    def get_queryset(self):
        estudiante_id = self.request.query_params.get('estudiante')
        if estudiante_id:
            return Alerta.objects.filter(estudiante_id=estudiante_id).order_by('-fecha')
        return Alerta.objects.all().order_by('-fecha')
