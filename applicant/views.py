from django.http.response import HttpResponse
from django.shortcuts import render
#from .models import Applicant

# Create your views here.
def applicantPageView(request):
    #a = App
    return render(request, "applicant/landing.html")

def skillsPageView(request):
    return render(request, "applicant/skills.html")

def resumePageView(request):
    return render(request, "applicant/resume.html")

def profilePageView(request):
    return render(request, "applicant/profile.html")

