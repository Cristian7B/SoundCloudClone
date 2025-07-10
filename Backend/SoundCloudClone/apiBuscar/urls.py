from django.urls import path
from .views import BuscarView, SugerenciasView

urlpatterns = [
    path('', BuscarView.as_view(), name='buscar'),
    path('sugerencias/', SugerenciasView.as_view(), name='sugerencias_busqueda'),
]
