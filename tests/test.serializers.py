import pytest
from authapp.models import Usuario, Persona, Estudiante, Rol
from usuarios.serializers import EstudianteUpdateSerializer
#from django.utils import timezone
from datetime import date
from rest_framework.exceptions import ValidationError

@pytest.fixture
def rol():
    return Rol.objects.create(nombre='Estudiante', descripcion='Rol estudiante')

@pytest.fixture
def usuario(rol):
    return Usuario.objects.create(username='juan', correo='juan@example.com', password='1234', rol=rol)

@pytest.fixture
def persona(usuario):
    return Persona.objects.create(
        usuario=usuario,
        ci='12345678',
        nombres='Juan',
        apellidos='Pérez',
        genero='M',
        fecha_nacimiento=date(2005, 5, 10),
        direccion='Calle Falsa 123',
        telefono='7654321'
    )

@pytest.fixture
def estudiante(persona):
    return Estudiante.objects.create(
        persona=persona,
        rude='RUDE123456'
    )

def test_estudiante_update_valid(estudiante):
    data = {
        'rude': 'RUDE999999',
        'persona': {
            'nombres': 'Juan Carlos',
            'telefono': '7000000',
            'usuario': {
                'username': 'juan_c',
                'correo': 'jc@example.com',
                'rol': estudiante.persona.usuario.rol.id,
                'password': 'nuevo123'
            }
        }
    }
    serializer = EstudianteUpdateSerializer(instance=estudiante, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.rude == 'RUDE999999'
    assert updated.persona.nombres == 'Juan Carlos'
    assert updated.persona.telefono == '7000000'
    assert updated.persona.usuario.username == 'juan_c'

def test_estudiante_update_invalid_rude(estudiante):
    Estudiante.objects.create(
        rude='RUDE_DUPLICADO',
        persona=estudiante.persona  # temporal para test
    )
    data = {'rude': 'RUDE_DUPLICADO'}
    serializer = EstudianteUpdateSerializer(instance=estudiante, data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

def test_persona_fecha_nacimiento_futura(estudiante):
    future_date = date.today().replace(year=date.today().year + 1)
    data = {
        'persona': {
            'fecha_nacimiento': future_date,
            'usuario': {
                'rol': estudiante.persona.usuario.rol.id
            }
        }
    }
    serializer = EstudianteUpdateSerializer(instance=estudiante, data=data, partial=True)
    assert not serializer.is_valid()
    assert 'fecha_nacimiento' in serializer.errors['persona']
