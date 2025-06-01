from django.apps import AppConfig


class EvaluacionEstudianteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evaluacion_estudiante'

    def ready(self):
        import evaluacion_estudiante.signals # noqa: F401
