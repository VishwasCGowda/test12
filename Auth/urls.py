from django.contrib import admin
from django.urls import path
from .views import register,login  # Import the register function directly

urlpatterns = [
    path('register', register),  # Use the imported register function
    path('login',login),
]
