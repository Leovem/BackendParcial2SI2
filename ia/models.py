# IA/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from authapp.models import Estudiante
from estructura_academica.models import GestionAcademica, Bimestre

class PrediccionML(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    gestion = models.ForeignKey(GestionAcademica, on_delete=models.RESTRICT)
    bimestre = models.ForeignKey(Bimestre, on_delete=models.RESTRICT)
    puntaje_predicho = models.DecimalField(max_digits=5, decimal_places=2)
    probabilidad_riesgo = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prediccion_ml'

class RecomendacionIA(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.RESTRICT)
    bimestre = models.ForeignKey(Bimestre, on_delete=models.RESTRICT)
    gestion = models.ForeignKey(GestionAcademica, on_delete=models.RESTRICT)
    recomendaciones = ArrayField(models.TextField())
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recomendaciones_ia'
