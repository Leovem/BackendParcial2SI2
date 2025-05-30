from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from authapp.models import Estudiante, Docente, PadreFamilia, Usuario, EstudiantePadre
from authapp.serializers import (EstudianteSerializer, EstudiantePadreSerializer)
from .serializers import (
    EstudianteReadSerializer,
    DocenteReadSerializer,
    PadreFamiliaReadSerializer,
    EstudianteUpdateSerializer,
    DocenteUpdateSerializer,
    PadreFamiliaUpdateSerializer,
    UsuarioUpdateSerializer
)



class ListarEstudiantesView(ListAPIView):
    queryset = Estudiante.objects.select_related('persona__usuario', 'persona__usuario__rol')
    serializer_class = EstudianteReadSerializer


class ListarDocentesView(ListAPIView):
    queryset = Docente.objects.select_related('persona__usuario', 'persona__usuario__rol')
    serializer_class = DocenteReadSerializer


class ListarPadresView(ListAPIView):
    queryset = PadreFamilia.objects.select_related('persona__usuario', 'persona__usuario__rol')
    serializer_class = PadreFamiliaReadSerializer

class EditarEstudianteView(APIView):
    def put(self, request, pk):
        try:
            estudiante = Estudiante.objects.get(pk=pk)
        except Estudiante.DoesNotExist:
            return Response({'detail': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #print("📥 Datos recibidos:", request.data)
        serializer = EstudianteUpdateSerializer(instance=estudiante, data=request.data, partial=True)
        

        if serializer.is_valid():
            #print("📦 validated_data:", serializer.validated_data)
            serializer.save()
            return Response({
                "mensaje": "Estudiante actualizado correctamente.",
                "datos": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EditarDocenteView(APIView):
    def put(self, request, pk):
        try:
            docente = Docente.objects.get(pk=pk)
        except Docente.DoesNotExist:
            return Response({'detail': 'Docente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocenteUpdateSerializer(instance=docente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EditarPadreFamiliaView(APIView):
    def put(self, request, pk):
        try:
            padre = PadreFamilia.objects.get(pk=pk)
        except PadreFamilia.DoesNotExist:
            return Response({'detail': 'Padre de familia no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PadreFamiliaUpdateSerializer(instance=padre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditarUsuarioView(APIView):
    def put(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioUpdateSerializer(instance=usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Usuario actualizado correctamente.",
                "datos": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HijosDePadreView(APIView):
    def get(self, request, padre_id):
        try:
            padre = PadreFamilia.objects.get(id=padre_id)
        except PadreFamilia.DoesNotExist:
            return Response({"detail": "Padre no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        relaciones = EstudiantePadre.objects.filter(padre=padre)
        estudiantes = [rel.estudiante for rel in relaciones]
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CrearRelacionEstudiantePadreView(generics.CreateAPIView):
    queryset = EstudiantePadre.objects.all()
    serializer_class = EstudiantePadreSerializer