from rest_framework import serializers
from authapp.models import Usuario, Persona, Estudiante, Docente, PadreFamilia, Rol
from django.contrib.auth.hashers import make_password
from datetime import date
from .mixins import NestedUpdateMixin


# --- ROL SERIALIZER ---
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']


# --- USUARIO READ SERIALIZER ---
class UsuarioReadSerializer(serializers.ModelSerializer):
    rol = RolSerializer()

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'correo', 'rol']


# --- PERSONA READ SERIALIZER ---
class PersonaReadSerializer(serializers.ModelSerializer):
    usuario = UsuarioReadSerializer()

    class Meta:
        model = Persona
        fields = ['id', 'ci', 'nombres', 'apellidos', 'genero', 'fecha_nacimiento', 'direccion', 'telefono', 'usuario']


# --- ESTUDIANTE READ SERIALIZER ---
class EstudianteReadSerializer(serializers.ModelSerializer):
    persona = PersonaReadSerializer()

    class Meta:
        model = Estudiante
        fields = ['id', 'rude', 'persona']


# --- DOCENTE READ SERIALIZER ---
class DocenteReadSerializer(serializers.ModelSerializer):
    persona = PersonaReadSerializer()

    class Meta:
        model = Docente
        fields = ['id', 'profesion', 'fecha_contratacion', 'persona']


# --- PADRE DE FAMILIA READ SERIALIZER ---
class PadreFamiliaReadSerializer(serializers.ModelSerializer):
    persona = PersonaReadSerializer()

    class Meta:
        model = PadreFamilia
        fields = ['id', 'persona']


# --- USUARIO UPDATE SERIALIZER ---
class UsuarioUpdateSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())

    class Meta:
        model = Usuario
        fields = ['id', 'rol', 'username', 'password', 'correo']
        extra_kwargs = {
            'password': {'write_only': True},
            'correo': {'validators': []},
            'username': {'validators': []},
        }

    def validate_username(self, value):
        if self.instance and value != self.instance.username and Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_correo(self, value):
        if self.instance and value != self.instance.correo and Usuario.objects.filter(correo=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value


    def validate_password(self, value):
        """Valida que la contraseña no esté vacía."""
        if value == "":
            raise serializers.ValidationError("La contraseña no puede estar vacía.")
        return value
    


    def update(self, instance, validated_data):
        """Actualiza la instancia del usuario con los datos validados."""
        print("🔥 UsuarioUpdateSerializer update ejecutado")
        password = validated_data.pop('password', None)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = make_password(password)

        instance.save()
        return instance
    


# --- PERSONA UPDATE SERIALIZER ---
class PersonaUpdateSerializer(serializers.ModelSerializer):
    usuario = UsuarioUpdateSerializer()

    class Meta:
        model = Persona
        fields = ['id', 'usuario', 'ci', 'nombres', 'apellidos', 'genero', 'fecha_nacimiento', 'direccion', 'telefono']
        extra_kwargs = {
            'ci': {'validators': []},
        }

    def validate_ci(self, value):
        if self.instance and value != self.instance.ci and Persona.objects.filter(ci=value).exists():
            raise serializers.ValidationError("Este CI ya está en uso.")
        return value


    def validate_fecha_nacimiento(self, value):
        """Valida que la fecha de nacimiento no sea futura."""
        if value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value

    def update(self, instance, validated_data):
        """Actualiza la instancia de la persona con los datos validados."""
        usuario_data = validated_data.pop('usuario', None)   

        if usuario_data and usuario_data != {}:
            usuario_serializer = UsuarioUpdateSerializer(instance=instance.usuario, data=usuario_data, partial=True)
            print("👀 usuario_data antes de serializar:", usuario_data)

            if 'rol' in usuario_data and isinstance(usuario_data['rol'], Rol):
                usuario_data['rol'] = usuario_data['rol'].id

            usuario_serializer.is_valid(raise_exception=True)
            print("👀 usuario_serializer.validated_data después de validar:", usuario_serializer.validated_data)
            usuario_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# --- ESTUDIANTE UPDATE SERIALIZER ---
class EstudianteUpdateSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    persona = PersonaUpdateSerializer()

    class Meta:
        model = Estudiante
        fields = ['id', 'persona', 'rude']

    def validate_rude(self, value):
        if value != self.instance.rude and Estudiante.objects.filter(rude=value).exists():
            raise serializers.ValidationError("Este RUDE ya está en uso.")
        return value

    def update(self, instance, validated_data):
        #print("🧪 Antes de nested update, rol es:", validated_data.get("persona", {}).get("usuario", {}).get("rol"))
        #print(validated_data)
        persona_data = validated_data.get('persona', {})

        if 'usuario' in persona_data:
            usuario_data = persona_data['usuario']

            # Si 'rol' es un objeto Rol, reemplazarlo por su id
            rol = usuario_data.get('rol')
            if hasattr(rol, 'id'):
                usuario_data['rol'] = rol.id

        # actualizar 'persona' con el usuario modificado
        persona_data['usuario'] = usuario_data
        validated_data['persona'] = persona_data
        #print(validated_data)
        self.update_nested_serializer(
            serializer_class=PersonaUpdateSerializer,
            instance_field='persona',
            parent_instance=instance,
            validated_data=validated_data,
            data_field_name='persona'
        )

        # Actualiza los campos del estudiante
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# --- DOCENTE UPDATE SERIALIZER ---
class DocenteUpdateSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    persona = PersonaUpdateSerializer()

    class Meta:
        model = Docente
        fields = ['id', 'persona', 'profesion', 'fecha_contratacion']

    def validate_fecha_contratacion(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de contratación no puede ser futura.")
        return value

    def update(self, instance, validated_data):
        persona_data = validated_data.get('persona', {})

        if 'usuario' in persona_data:
            usuario_data = persona_data['usuario']

            # Si 'rol' es un objeto Rol, reemplazarlo por su id
            rol = usuario_data.get('rol')
            if hasattr(rol, 'id'):
                usuario_data['rol'] = rol.id

        # actualizar 'persona' con el usuario modificado
        persona_data['usuario'] = usuario_data
        validated_data['persona'] = persona_data
        self.update_nested_serializer(
            serializer_class=PersonaUpdateSerializer,
            instance_field='persona',
            parent_instance=instance,
            validated_data=validated_data,
            data_field_name='persona'
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



# --- PADRE DE FAMILIA UPDATE SERIALIZER ---
class PadreFamiliaUpdateSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    persona = PersonaUpdateSerializer()

    class Meta:
        model = PadreFamilia
        fields = ['id', 'persona']

    def update(self, instance, validated_data):
        persona_data = validated_data.get('persona', {})

        if 'usuario' in persona_data:
            usuario_data = persona_data['usuario']

            # Si 'rol' es un objeto Rol, reemplazarlo por su id
            rol = usuario_data.get('rol')
            if hasattr(rol, 'id'):
                usuario_data['rol'] = rol.id

        # actualizar 'persona' con el usuario modificado
        persona_data['usuario'] = usuario_data
        validated_data['persona'] = persona_data
        self.update_nested_serializer(
            serializer_class=PersonaUpdateSerializer,
            instance_field='persona',
            parent_instance=instance,
            validated_data=validated_data,
            data_field_name='persona'
        )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


