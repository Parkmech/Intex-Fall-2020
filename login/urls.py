from os import name
from django.urls import path
from .views import candidateLoginView,employerLoginView, employerSignUpView,candidateSignUpView

urlpatterns = [
    path('employer/login', employerLoginView, name='employerLogin'),
    path('employer/signup', employerSignUpView, name='employerSignup'),
    path('applicant/signup',candidateSignUpView, name='applicantSignup'),
    path('applicant/login', candidateLoginView, name='applicantLogin'),
    path('', candidateSignUpView, name='applicantSignup'),
]
