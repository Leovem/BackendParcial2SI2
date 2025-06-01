from django.db import models
from estructura_academica.models import Bimestre
from authapp.models import Estudiante
from inscripcion.models import Curso, Materia

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    materia = models.ForeignKey(Materia, on_delete=models.RESTRICT)
    bimestre = models.ForeignKey(Bimestre, on_delete=models.RESTRICT)
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    observacion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (0 <= self.nota <= 100):
            raise ValidationError("La nota debe estar entre 0 y 100")

    class Meta:
        db_table = 'calificacion'


class Asistencia(models.Model):
    ESTADOS = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tardanza', 'Tardanza'),
        ('justificado', 'Justificado'),
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    materia = models.ForeignKey(Materia, on_delete=models.RESTRICT)
    bimestre = models.ForeignKey(Bimestre, on_delete=models.RESTRICT)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    justificacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'asistencia'


class Participacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    materia = models.ForeignKey(Materia, on_delete=models.RESTRICT)
    bimestre = models.ForeignKey(Bimestre, on_delete=models.RESTRICT)
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)  # Ej: tarea, exposición
    descripcion = models.TextField(blank=True, null=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.puntaje < 0:
            raise ValidationError("El puntaje no puede ser negativo.")

    class Meta:
        db_table = 'participacion'
