import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class SugerenciaCancionesView(APIView):
    def get(self, request):
        todas_canciones = list(Cancion.objects.all())

        if len(todas_canciones) == 0:
            return Response({"mensaje": "No hay canciones disponibles."}, status=status.HTTP_404_NOT_FOUND)

        canciones_aleatorias = random.sample(todas_canciones, min(3, len(todas_canciones)))
        canciones_serializadas = CancionSerializer(canciones_aleatorias, many=True)

        return Response(canciones_serializadas.data, status=status.HTTP_200_OK)
