from django.db import models


class Curso(models.Model):
    grado = models.ForeignKey('estructura_academica.Grado', on_delete=models.RESTRICT)
    paralelo = models.CharField(max_length=1)
    gestion = models.ForeignKey('estructura_academica.GestionAcademica', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'curso'

    def __str__(self):
        return f'{self.grado.nombre}{self.paralelo} - {self.gestion.anio}'


class Inscripcion(models.Model):
    estudiante = models.ForeignKey('authapp.Estudiante', on_delete=models.RESTRICT)
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    gestion = models.ForeignKey('estructura_academica.GestionAcademica', on_delete=models.RESTRICT)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'inscripcion'
        unique_together = ('estudiante', 'curso', 'gestion')


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

    class Meta:
        db_table = 'materia'

    def __str__(self):
        return self.nombre


class CursoMateria(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    materia = models.ForeignKey(Materia, on_delete=models.RESTRICT)
    docente = models.ForeignKey('authapp.Docente', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'curso_materia'


class HorarioClase(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ]

    curso_materia = models.ForeignKey(CursoMateria, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'horario_clase'
        ordering = ['dia_semana', 'hora_inicio']

    def __str__(self):
        return f'{self.curso_materia} - {self.dia_semana} {self.hora_inicio}-{self.hora_fin}'

