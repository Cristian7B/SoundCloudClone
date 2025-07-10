from django.urls import path
from .views import SugerenciaCancionesView

urlpatterns = [
    path('sugerencias/', SugerenciaCancionesView.as_view(), name='sugerencias-canciones'),
]
