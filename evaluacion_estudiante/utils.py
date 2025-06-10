# utils.py
from estructura_academica.models import GestionAcademica

def obtener_ultima_gestion():
    return GestionAcademica.objects.order_by('-anio').first()
