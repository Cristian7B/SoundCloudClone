import envirion
import os
import requests

from google.auth.transport import requests

from rest_framework import generics, status
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


env = envirion.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        serializer_class = UserRegisterSerializer(request.data)

        try:
            serializer_class.is_valid(raise_exception=True)
            databaseurl = env('DATABASE_SERVICE_URL')
            response = requests.post(f'{databaseurl}/register_user', data = request.data)

            if response.status  != 201:
                return Response({'error' : 'Error registrando nuevo usuario.'}, status = status.HTTP_504_GATEWAY_TIMEOUT)
            
            return Response(response.json(), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error_message' : 'Error registrando nuevo usuario.'}, status = status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user

        databaseurl = env('DATABASE_SERVICE_URL')
        response = requests.get(f'{databaseurl}/getUserInfo', params = user)

        if response.status != 200:
            return Response({'error': 'Error obteniendo la informacion del usuario'}, status=status.HTTP_504_GATEWAY_TIMEOUT )
        
        return Response(response.json(), status=status.HTTP_200_OK)
    
class UpdateUserInfo(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer_class = UserUpdateSerializer(request.user, data=request.data)

        if serializer_class.is_valid():
            databaseurl = env('DATABASE_SERVICE_URL')
            response = requests.post(f'{databaseurl}/update_user_info', data=request.data)

            if response.status != 200:
                return Response({'error': 'Error actualizando los datos del usuario'}, status = status.HTTP_504_GATEWAY_TIMEOUT)
        
            return Response(response.json(), status = status.HTTP_200_OK)
        return Response({'error': 'Error validando datos del usuario'}, status.status.HTTP_400_BAD_REQUEST)

class UserLogin(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)

        databaseurl = env('DATABASE_SERVICE_URL')
        response = requests.post(f'{databaseurl}/login_user', data = data)

        if response.status != 200:
            return Response({'error_message' : 'Error al iniciar sesion.'}, status = status.HTTP_400_BAD_REQUEST)
        
        return Response(response.json(), status = status.HTTP_200_OK)
    
class UserLogout(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        logout(request)
        return Response(status = status.HTTP_200_OK)
