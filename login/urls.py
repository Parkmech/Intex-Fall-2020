from os import name
from django.urls import path
from .views import employerLoginView, candidateLoginView, employerLoginForm, employerSignUpView,candidateSignUpView, candidateLoginForm

urlpatterns = [
    path('employer/login', employerLoginView, name='employerLogin'),
    path('employer/signup', employerSignUpView, name='employerSignup'),
    path('applicant/signup',candidateSignUpView, name='applicantSignup'),
    path('applicant/login', candidateLoginView, name='applicantLogin'),
    path('employer/loginForm', employerLoginForm, name='empLoginForm'),
    path('applicant/LoginForm', candidateLoginForm, name='candidateLoginForm'),
    path('', candidateLoginView, name='applicantLogin'),
]
