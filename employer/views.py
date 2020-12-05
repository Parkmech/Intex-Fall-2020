from django import http
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def employerPageView(request):
    return render(request, "employer/landing.html")

def employerSkillView(request):
    return render(request, "employer/skills.html")

def employerProfileView(request):
    return render(request, "employer/profile.html")

def employerCreateView(request):
    return render(request, 'employer/createlisting.html')

def employerEditView(request):
    return render(request, "employer/editlisting.html")


