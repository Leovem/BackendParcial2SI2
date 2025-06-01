from django.db import models
from authapp.models import Estudiante

class Alerta(models.Model):
    TIPO_CHOICES = [
        ('falta', 'Falta de asistencia'),
        ('nota baja', 'Nota baja'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')  # pendiente, revisada

    class Meta:
        db_table = 'alerta'

    def __str__(self):
        return f'{self.tipo} - {self.estudiante}'
