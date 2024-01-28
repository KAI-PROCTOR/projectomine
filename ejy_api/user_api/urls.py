from django.contrib import admin
from django.urls import path
from . import views
from .views import Registeruser,LoginView,LogoutView
from .views import ForgotPasswordView, ResetPasswordview, GetUserInfoView,ChangePasswordView,EditProfileView





urlpatterns=[
    path('registeruser/', Registeruser.as_view(), name='register'),
path('login/', LoginView.as_view(), name='login'),
path('logout/', LogoutView.as_view(), name='logout'),
path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
path('change-password/', ChangePasswordView.as_view(), name='change-password'),
path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
path('reset-password/<str:token>/', ResetPasswordview.as_view(), name='reset-forgotten-password'),
path('getinfouser/<int:id>/', GetUserInfoView.as_view(), name='get-user-info'),
]