from django.contrib.auth import aauthenticate

from rest_framework import generics, status
from rest_framework.response import responses
from rest_framework.permissions import  IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *

class RegistroCancionView(generics.CreateAPIView):
          def post(self,request):
                    serializer_class = RegistroCancion(data=request.data)
                    if serializer_class.is_valid():
                              serializer_class.save()
                              return Response({'message' : 'La cancion se ha registrado'}, status=status.HTTP_201_CREATED)
                    return Response({'error' : 'No se pudo registrar la cancion'}, status=status.HTTP_400_BAD_REQUEST)

class RegistroPlayListView(generics.CreateAPIView):
          def post(self,request):
                    serializer_class = RegistroPlayList(data = request.data)
                    if serializer_class.is_valid():
                              serializer_class.save()
                              return Response({'message' : 'Se ha creado la playlist'}, status=status.HTTP_201_CREATED)
                    return Response({'error' : 'No se pudo crear la playlist'}, status=status.HTTP_400_BAD_REQUEST)

class GetUserInfo(generics.CreateAPIView):
          permission_classes = (IsAuthenticated,)
          def get(self,request):
                    user = request.user
                    try:
                              user_info = UserModel.objects.get(email=user.email)
                              user_data = {
                                        'email' : user_info.email,
                                        'username' : user_info.username,
                                        'nombre' : user_info.nombre,
                                        'created_at' : user_info.created_at,
                              }
                              return Response(user_data, status=status.HTTP_200_OK)
                    except UserModel.DoesNotExist:
                              return Response({'error' : 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserInfo(generics.CreateAPIView):
          permission_classes = (IsAuthenticated,)
          def post(self, request):
                    user = request.user
                    serializer_class = UserUpdateSerializer(user, data=request.data)
                    if serializer_class.is_valid():
                              serializer_class.save()
                              return Response(serializer_class.data, status=status.HTTP_200_OK)
                    return Response({'error' : 'Error actualizando los datos'}, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(generics.CreateAPIView):
          permission_classes = (IsAuthenticated,)

          def post(self, request):
                    email = request.data.get('email')
                    password = request.data.get('password')

                    user = aauthenticate(username = email, password = password)

                    if user:
                              refresh = RefreshToken.for_user(user)
                              return Response({
                                        'refresh' : str(refresh),
                                        'access' : str(refresh.access_token),
                                        'user' : UserRegisterSerializer(user).data
                              }, status=status.HTTP_200_OK)
                    return Response({'error' : 'Credenciales no validas'}, status=status.HTTP_400_BAD_REQUEST)

class CheckUserExist(generics.CreateAPIView):
          def get(self, request):
                    email = request.query_params.get('email')

                    try:
                              user = UserModel.objects.get(email = email)
                              return Response({'exists' : True, 'user' : UserRegisterSerializer(user).data}, status = status.HTTP_200_OK)
                    except UserModel.DoesNotExist:
                              return Response({'exists' : False}, status= status.HTTP_200_OK)
