from django.urls import path
from .views import RegistroUsuarioView, LoginUsuarioView 

urlpatterns = [
    path('registrar/', RegistroUsuarioView.as_view(), name='registro-usuario'),
    path('login/', LoginUsuarioView.as_view(), name='login_usuario'),
]
