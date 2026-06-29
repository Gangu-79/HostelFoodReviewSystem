from django.urls import path
from .views import register, feedback
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/register/')),
    path('register/', register, name='register'),
    path('feedback/', feedback, name='feedback'),
]