from django.db.models.signals import post_save
from django.dispatch import receiver
from evaluacion_estudiante.models import Asistencia, Calificacion
from alertas.models import Alerta

@receiver(post_save, sender=Asistencia)
def generar_alerta_asistencia(sender, instance, **kwargs):
    if instance.estado == 'ausente':
        Alerta.objects.create(
            estudiante=instance.estudiante,
            tipo='falta',
            descripcion=f"Falta registrada el {instance.fecha} en {instance.materia}",
        )

@receiver(post_save, sender=Calificacion)
def generar_alerta_nota_baja(sender, instance, **kwargs):
    if instance.nota < 51:
        Alerta.objects.create(
            estudiante=instance.estudiante,
            tipo='nota baja',
            descripcion=f"Nota baja ({instance.nota}) en {instance.materia}",
        )
