# apiAutenticacion/urls.py
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('update_info/', UserUpdateInfo.as_view(), name = 'update_info'),
    path('logout', UserLogout.as_view(), name = 'logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
