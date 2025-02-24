
from django.contrib import admin
from django.urls import path, include
from myprojectdpoll import views
from .views import register_voter

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("api/register/", register_voter),
]
