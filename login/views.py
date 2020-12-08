from applicant.models import Applicant
from django.shortcuts import render, redirect
from django.http import HttpResponse
import applicant.urls
import employer.urls

# from .users import set_user
# from .users import current_user
# from .users import get_user
# Create your views here.

def candidateLoginForm(request):
    username = request.POST.get('username')
    password = 'password'
    return redirect('applicant')

def employerLoginForm(request):
    return redirect('employer')

def candidateLoginView(request):
    return render(request, 'login/candidatelogin.html')

def employerLoginView(request):
    return render(request, "login/employerlogin.html")

def employerSignUpView(request):
    return render(request, "login/employersignup.html")

def candidateSignUpView(request):
    return render(request, "login/candidatesignup.html")


