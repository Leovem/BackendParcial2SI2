from rest_framework import viewsets
from .models import Nivel, Grado, GestionAcademica, Bimestre
from .serializers import NivelSerializer, GradoSerializer, GestionAcademicaSerializer, BimestreSerializer

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

class GradoViewSet(viewsets.ModelViewSet):
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer

class GestionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = GestionAcademica.objects.all()
    serializer_class = GestionAcademicaSerializer

class BimestreViewSet(viewsets.ModelViewSet):
    queryset = Bimestre.objects.all()
    serializer_class = BimestreSerializer
