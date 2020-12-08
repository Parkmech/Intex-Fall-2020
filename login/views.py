from applicant.models import Applicant, Organization
from django.shortcuts import render, redirect
from django.http import HttpResponse
import applicant.urls
import employer.urls

# from .users import set_user
# from .users import current_user
# from .users import get_user
# Create your views here
def getEmployerInfo():
    file = open('current_employer.txt', 'r')
    current_user =  int(file.readline())
    return current_user

def setEmployerInfo(user_id):
    file = open('current_employer.txt', 'w')
    file.write(str(user_id))
    file.close()

def getUserInfo():
    file = open('current_user.txt', 'r')
    current_user =  int(file.readline())
    return current_user

def setUserInfo(user_id):
    file = open('current_user.txt', 'w')
    file.write(str(user_id))
    file.close()

def candidateLoginForm(request):
    username = request.POST.get('username')
    password = 'password'
    user = Applicant.objects.get(username=username, password = password)
    setUserInfo(user.id)
    print('-------------------------LOGIN---------------------')
    print(getUserInfo())
    return redirect('applicant')

def employerLoginForm(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = Organization.objects.get(email=email, password = password)
    setEmployerInfo(user.id)
    print('-------------------------EMPLOYER---------------------')
    print(getEmployerInfo())
    return redirect('employer')

def candidateLoginView(request):
    return render(request, 'login/candidatelogin.html')

def employerLoginView(request):
    return render(request, "login/employerlogin.html")

def employerSignUpView(request):
    return render(request, "login/employersignup.html")

def candidateSignUpView(request):
    return render(request, "login/candidatesignup.html")


