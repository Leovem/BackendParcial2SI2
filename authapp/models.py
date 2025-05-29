from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinLengthValidator


class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash y asignación en password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')

        return self.create_user(username, password, **extra_fields)


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'roles'
        managed = True  # Cámbialo a True si vas a migrar desde Django

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    correo = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo']
    EMAIL_FIELD = 'correo'

    class Meta:
        db_table = 'usuario'
        managed = False  # Cámbialo a True si vas a usar makemigrations

    def __str__(self):
        return self.username
    
class Persona(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    ci = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(5)])
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    genero = models.CharField(max_length=10, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'persona'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Estudiante(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    rude = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'estudiante'

    def __str__(self):
        return f"Estudiante: {self.persona}"


class Docente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    profesion = models.CharField(max_length=100, null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'docente'

    def __str__(self):
        return f"Docente: {self.persona}"


class PadreFamilia(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

    class Meta:
        db_table = 'padre_familia'

    def __str__(self):
        return f"Padre/Tutor: {self.persona}"


class EstudiantePadre(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    padre = models.ForeignKey(PadreFamilia, on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=30)

    class Meta:
        db_table = 'estudiante_padre'

    def __str__(self):
        return f"{self.padre} - {self.estudiante} ({self.parentesco})"
