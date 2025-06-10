# mixins.py
from inscripcion.utils import obtener_ultima_gestion

class UltimaGestionMixin:
    def get_gestion_id(self, request):
        gestion_id = request.query_params.get('gestion_id')
        if gestion_id:
            return gestion_id
        return obtener_ultima_gestion().id
