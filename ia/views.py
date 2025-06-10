from rest_framework import viewsets
from .models import PrediccionML, RecomendacionIA
from .serializers import PrediccionMLSerializer, RecomendacionIASerializer

class PrediccionMLViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrediccionML.objects.all()
    serializer_class = PrediccionMLSerializer

class RecomendacionIAViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecomendacionIA.objects.all()
    serializer_class = RecomendacionIASerializer