from django.urls import path
from rest_framework.authtoken import views

from rest_framework import routers

urlpatterns = [
    path('auth/', views.obtain_auth_token),
]
