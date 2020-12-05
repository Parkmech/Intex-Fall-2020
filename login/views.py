from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def candidateLoginView(request):
    return render(request, "login/candidatelogin.html")

def employerLoginView(request):
    return render(request, "login/employerlogin.html")

def employerSignUpView(request):
    return render(request, "login/employersignup.html")

def candidateSignUpView(request):
    return render(request, "login/candidatesignup.html")


