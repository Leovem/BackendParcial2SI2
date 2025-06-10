from django.db import models
from authapp.models import Estudiante
from estructura_academica.models import GestionAcademica, Bimestre

class ResumenRendimiento(models.Model):
    NIVEL_RIESGO_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    gestion = models.ForeignKey(GestionAcademica, on_delete=models.RESTRICT)
    bimestre = models.ForeignKey(Bimestre, on_delete=models.RESTRICT)

    promedio_notas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentaje_asistencia = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    puntaje_participacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    nivel_riesgo = models.CharField(max_length=20, choices=NIVEL_RIESGO_CHOICES, blank=True, null=True)
    patrones_comportamiento = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'resumen_rendimiento'
        unique_together = ('estudiante', 'gestion', 'bimestre')

    def __str__(self):
        return f"Resumen {self.estudiante} - B{self.bimestre.id} ({self.nivel_riesgo})"
