from django.urls import path
from .views import *

urlpatterns = [
          path('registrar_cancion/', RegistroCancionView.as_view(), name = 'registro_cancion' ),
          path('registrar_playlist/', RegistroPlayListView.as_view(), name = 'registro_playlist')
]