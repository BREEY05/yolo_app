from django.urls import path
from . import views

urlpatterns = [
    path('send_code/', views.send_verification_code, name='send_code'),
    path('register/', views.register_with_code, name='register'),
    path('login/', views.login_with_password, name='login'),
]
