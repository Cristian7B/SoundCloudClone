from rest_framework import serializers
from SoundCloudClone.models import *

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
          class Meta:
                    model = UserModel
                    fields = '__all__'
                    extra_kwargs = {
                              'password' : {'write_only' : True},
                    }
          
          def create(self,validated_data):
                    user = UserModel.objects.create_user(
                              email = validated_data['email'],
                              password = validated_data['password'],
                              username = validated_data['username']
                    )
                    return user

class UserLoginSerializer(serializers.ModelSerializer):
          username = serializers.CharField()
          email = serializers.EmailField()
          password = serializers.CharField()

          def check_user(self, clean_data):
                    user = authenticate(username = clean_data['username'], email = clean_data['email'], password = clean_data['password'])
                    if not user:
                              raise ValidationError('User not found')
                    return user

class UserSerializer(serializers.ModelSerializer):
          class Meta:
                    model = User
                    fields = ('username', 'email', 'password')

class UserUpdateSerializer(serializers.ModelSerializer):
          class Meta: 
                    model = User
                    fields = ['username', 'email']

class RegistroCancion(serializers.ModelSerializer):
          class Meta:
                    model = Cancion
                    fields = ['titulo', 'archivo_url', 'usuario', 'created_at']

class RegistroPlayList(serializers.ModelSerializer):
          class Meta:
                    model = Playlist
                    fields = ['titulo', 'usuario', 'created_at']
