# apiAutenticacion/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, UpdateUserInfo, UserLogout, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('update-info/', UpdateUserInfo.as_view(), name='update_info'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
