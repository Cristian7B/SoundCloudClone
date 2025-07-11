import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apiPersistencia.models import Cancion
from apiBuscar.serializers import CancionSerializer

class SugerenciaCancionesView(APIView):
    """
        Vista para sugerir canciones aleatorias.

        Endpoint: GET /sugerencias/canciones/

        Retorna:
            {
                "mensaje": "Se encontraron X canciones sugeridas",
                "canciones": [
                    {
                        "cancion_id": int,
                        "titulo": str,
                        "archivo_url": str,
                        "imagen_url": str,
                        "duracion": time,
                        "genero": str,
                        "usuario_id": int,
                        "reproducciones": int,
                        "likes_count": int,
                        "created_at": datetime
                    },
                    ...
                ]
            }

        Permisos: Acceso público
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        todas_canciones = list(Cancion.objects.all())

        if len(todas_canciones) == 0:
            return Response({
                "mensaje": "No hay canciones disponibles."
            }, status=status.HTTP_404_NOT_FOUND)

        # Tomar 5 canciones aleatorias
        cantidad = min(5, len(todas_canciones))
        canciones_aleatorias = random.sample(todas_canciones, cantidad)
        canciones_serializadas = CancionSerializer(canciones_aleatorias, many=True)

        return Response({
            "mensaje": f"Se encontraron {cantidad} canciones sugeridas",
            "canciones": canciones_serializadas.data
        }, status=status.HTTP_200_OK)
