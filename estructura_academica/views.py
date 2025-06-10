from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Nivel, Grado, GestionAcademica, Bimestre
from .serializers import NivelSerializer, GradoSerializer, GestionAcademicaSerializer, BimestreSerializer

class NivelViewSet(viewsets.ModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer

class GradoViewSet(viewsets.ModelViewSet):
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer

    @action(detail=False, methods=['get'], url_path='por-nivel/(?P<nivel_id>\d+)')
    def por_nivel(self, request, nivel_id=None):
        grados = Grado.objects.filter(nivel_id=nivel_id)
        serializer = self.get_serializer(grados, many=True)
        return Response(serializer.data)

class GestionAcademicaViewSet(viewsets.ModelViewSet):
    queryset = GestionAcademica.objects.all()
    serializer_class = GestionAcademicaSerializer

class BimestreViewSet(viewsets.ModelViewSet):
    queryset = Bimestre.objects.all()
    serializer_class = BimestreSerializer


class BimestresPorAnioView(APIView):
    def get(self, request, anio):
        bimestres = Bimestre.objects.filter(gestion__anio=anio)
        serializer = BimestreSerializer(bimestres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UltimaGestionView(APIView):
    def get(self, request):
        ultima = GestionAcademica.objects.order_by('-anio').first()
        serializer = GestionAcademicaSerializer(ultima)
        return Response(serializer.data)

