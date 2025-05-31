from django.db import models
from django.core.exceptions import ValidationError

class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'nivel'

    def __str__(self):
        return self.nombre

class Grado(models.Model):
    nivel = models.ForeignKey(Nivel, on_delete=models.RESTRICT, related_name='grados')
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'grado'

    def __str__(self):
        return f'{self.nombre} - {self.nivel.nombre}'

class GestionAcademica(models.Model):
    anio = models.IntegerField(unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'gestion_academica'

    def __str__(self):
        return str(self.anio)

    def clean(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')

class Bimestre(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    gestion = models.ForeignKey(GestionAcademica, on_delete=models.RESTRICT, related_name='bimestres')

    class Meta:
        db_table = 'bimestre'

    def __str__(self):
        return f'{self.nombre} - {self.gestion.anio}'

    def clean(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
