from django.urls import path
from .views import (
    RegistroCancionView, 
    RegistroPlayListView, 
    GetUserInfo, 
    UpdateUserInfo, 
    LoginUser, 
    CheckUserExist
)

urlpatterns = [
    path('register-song/', RegistroCancionView.as_view(), name='register_song'),
    path('register-playlist/', RegistroPlayListView.as_view(), name='register_playlist'),
    path('user-info/', GetUserInfo.as_view(), name='get_user_info'),
    path('update-user/', UpdateUserInfo.as_view(), name='update_user_info'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('check-user/', CheckUserExist.as_view(), name='check_user_exists'),
]