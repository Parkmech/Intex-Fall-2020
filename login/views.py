from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def candidateLoginView(request):
    return HttpResponse('Default Login Page (Candidate)')

def employerLoginView(request):
    return HttpResponse('Employer Login Page')

def employerSignUpView(request):
    return HttpResponse('Employer Sign up Page')

def candidateSignUpView(request):
    return HttpResponse('Candidate Sign up Page')


