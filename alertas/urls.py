from django.urls import path
from .views import AlertaListView

urlpatterns = [
    path('listar/', AlertaListView.as_view(), name='listar-alertas'),
]
