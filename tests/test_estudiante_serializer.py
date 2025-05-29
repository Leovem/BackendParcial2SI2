import pytest
from authapp.models import Rol, Usuario, Persona, Estudiante
from usuarios.serializers import EstudianteUpdateSerializer

@pytest.fixture
def rol_estudiante():
    return Rol.objects.create(nombre='Estudiante', descripcion='Rol del estudiante')

@pytest.fixture
def usuario(rol_estudiante):
    return Usuario.objects.create(username='est123', correo='est@mail.com', password='123', rol=rol_estudiante)

@pytest.fixture
def persona(usuario):
    return Persona.objects.create(
        usuario=usuario,
        ci='3333333',
        nombres='Pedro',
        apellidos='Cruz',
        genero='M',
        fecha_nacimiento='2005-06-15',
        direccion='Calle A',
        telefono='71234567'
    )

@pytest.fixture
def estudiante(persona):
    return Estudiante.objects.create(persona=persona, rude='RUDE0001')

def test_estudiante_update_completo(estudiante, rol_estudiante):
    data = {
        'rude': 'RUDE20259999',
        'persona': {
            'nombres': 'Pedro Pablo',
            'telefono': '76543210',
            'usuario': {
                'username': 'pedrop',
                'correo': 'pedro.pablo@mail.com',
                'rol': rol_estudiante.id,
                'password': 'nuevaclave456'
            }
        }
    }

    serializer = EstudianteUpdateSerializer(instance=estudiante, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors

    estudiante_actualizado = serializer.save()

    assert estudiante_actualizado.rude == 'RUDE9999'
    assert estudiante_actualizado.persona.nombres == 'Pedro Pablo'
    assert estudiante_actualizado.persona.telefono == '76543210'
    assert estudiante_actualizado.persona.usuario.username == 'pedrop'
    assert estudiante_actualizado.persona.usuario.correo == 'pedro.pablo@mail.com'
