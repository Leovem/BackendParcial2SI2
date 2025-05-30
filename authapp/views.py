from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import EstudianteSerializer, DocenteSerializer, PadreFamiliaSerializer, UsuarioSerializer

class LoginUsuarioView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Se requieren 'username' y 'password'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Autenticar al usuario
        usuario = authenticate(username=username, password=password)

        if usuario:
            # Serializar los datos completos del usuario
            serializer = UsuarioSerializer(usuario)

            # Retornar respuesta con info del usuario, incluyendo rol
            return Response({
                "mensaje": "Inicio de sesión exitoso.",
                "usuario": {
                    "id": usuario.id,
                    "username": usuario.username,
                    "correo": usuario.correo,
                    "rol": usuario.rol.nombre
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciales inválidas."},
                            status=status.HTTP_401_UNAUTHORIZED)


class RegistroUsuarioView(APIView):
    def post(self, request):
        try:
            datos = request.data.copy()
            print(datos)
            rol_id = datos.get("persona", {}).get("usuario", {}).get("rol")
            print(rol_id)

            if not rol_id:
                return Response({"error": "El campo 'rol' es obligatorio en usuario."},
                                status=status.HTTP_400_BAD_REQUEST)

            rol_nombre = None

            # Se detecta el tipo de usuario por nombre del rol (solo si no es admin)
            from .models import Rol
            try:
                rol_obj = Rol.objects.get(id=rol_id)
                rol_nombre = rol_obj.nombre.lower()
            except Rol.DoesNotExist:
                return Response({"error": f"Rol con id {rol_id} no existe."},
                                status=status.HTTP_400_BAD_REQUEST)

            if rol_nombre == "estudiante":
                serializer = EstudianteSerializer(data=datos)
            elif rol_nombre == "docente":
                serializer = DocenteSerializer(data=datos)
            elif rol_nombre == "padre":
                serializer = PadreFamiliaSerializer(data=datos)
            elif rol_nombre == "admin":
                usuario_data = datos.get("persona", {}).get("usuario", {})
                serializer = UsuarioSerializer(data=usuario_data)
            else:
                return Response({"error": f"Rol '{rol_nombre}' no soportado."},
                                status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                entidad = serializer.save()

                if rol_nombre == "admin":
                    return Response({
                        "mensaje": "Administrador registrado exitosamente.",
                        "usuario": {
                            "id": entidad.id,
                            "username": entidad.username,
                            "correo": entidad.correo,
                            "rol": entidad.rol.nombre
                        }
                    }, status=status.HTTP_201_CREATED)

                return Response({
                    "mensaje": f"{rol_nombre.capitalize()} registrado exitosamente.",
                    "id": entidad.id
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Ocurrió un error: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

