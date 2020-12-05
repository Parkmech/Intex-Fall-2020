from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def applicantPageView(request):
    return HttpResponse("Applicant Page")

def skillsPageView(request):
    return HttpResponse("Skills Page")

def resumePageView(request):
    return HttpResponse("Resume Page")

def profilePageView(request):
    return HttpResponse("Profile Page")

