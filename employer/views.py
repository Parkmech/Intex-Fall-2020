from django import http
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def employerPageView(request):
    return HttpResponse("Employer Page")

def employerSkillView(request):
    return HttpResponse("Employer Skill Page")

def employerProfileView(request):
    return HttpResponse("Employer Profile")

def employerCreateView(request):
    return HttpResponse("Employer Create Listing Page")

def employerEditView(request):
    return HttpResponse("Employer Edit Listing Page")


