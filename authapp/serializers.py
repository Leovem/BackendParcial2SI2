from rest_framework import serializers
from .models import Usuario, Persona, Estudiante, Docente, PadreFamilia, Rol, EstudiantePadre
from django.contrib.auth.hashers import make_password


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre', 'descripcion']


class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all()
    )

    class Meta:
        model = Usuario
        fields = ['id', 'rol', 'username', 'password', 'correo']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def validate(self, data):
        username = data.get('username')
        correo = data.get('correo')

        if Usuario.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Este nombre de usuario ya está en uso."})
        if correo and Usuario.objects.filter(correo=correo).exists():
            raise serializers.ValidationError({"correo": "Este correo electrónico ya está en uso."})
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data) 
    






class PersonaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Persona
        fields = ['id', 'usuario', 'ci', 'nombres', 'apellidos', 'genero', 'fecha_nacimiento', 'direccion', 'telefono']

    def validate(self, data):
        ci = data.get('ci')
        instance_id = self.instance.id if self.instance else None

        if Persona.objects.filter(ci=ci).exclude(id=instance_id).exists():
            raise serializers.ValidationError({"ci": "Este CI ya está en uso."})
        return data

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')

        # ✅ Asegurar que 'rol' sea un ID, no un objeto Rol
        if isinstance(usuario_data.get("rol"), Rol):
            usuario_data["rol"] = usuario_data["rol"].id

        usuario_serializer = UsuarioSerializer(data=usuario_data)
        usuario_serializer.is_valid(raise_exception=True)
        usuario = usuario_serializer.save()

        return Persona.objects.create(usuario=usuario, **validated_data)
    


class EstudianteSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Estudiante
        fields = ['id', 'persona', 'rude']

    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona = PersonaSerializer().create(persona_data)
        return Estudiante.objects.create(persona=persona, **validated_data)
    



class DocenteSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = Docente
        fields = ['id', 'persona', 'profesion', 'fecha_contratacion']

    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona = PersonaSerializer().create(persona_data)
        return Docente.objects.create(persona=persona, **validated_data)
    



class PadreFamiliaSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()

    class Meta:
        model = PadreFamilia
        fields = ['id', 'persona']

    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona = PersonaSerializer().create(persona_data)
        return PadreFamilia.objects.create(persona=persona)
    
class EstudiantePadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudiantePadre
        fields = '__all__'

