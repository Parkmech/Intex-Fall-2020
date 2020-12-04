from os import name
from django.urls import path
from .views import loginPageView

urlpatterns = [
    path('', loginPageView, name='login'),
]
