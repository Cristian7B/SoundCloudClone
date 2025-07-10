from django.urls import path
from .views import SugerenciaCancionesView

urlpatterns = [
    path('', SugerenciaCancionesView.as_view(), name='sugerencias-canciones'),
]
