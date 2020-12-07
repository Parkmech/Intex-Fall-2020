from applicant.models import PreferredSkill
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from applicant.models import Applicant, ApplicantSkill, PreferredSkill, Listing, Skill


# Create your views here.
def employerPageView(request):
    A = Applicant.objects.all()
    applicants = []
    for i in A:
        applicants.append(i)
    applicants = applicants[0:20]
    skills = ApplicantSkill.objects.all()
    print('------', len(applicants))
        
    
    context = {
        'applicants' : applicants,
        'skills' : skills
    }
    return render(request, "employer/landing.html", context)

def employerSkillView(request):
    listing_id = 3
    s = PreferredSkill.objects.all()
    skills = []
    for i in s:
        if i.listing.id == listing_id:
            skills.append(i)
    print(len(skills))
    context = {
        'skills' : skills
    }
    return render(request, "employer/skills.html", context)

def addPreferredSkills (request) :

    skill_id = request.POST.get("skill")
    level = request.POST.get("level")
    listing_id = ''

    prefSkill = PreferredSkill(level=level, listing_id=listing_id, skill_id=skill_id)
    prefSkill.save()

    return redirect("skills")

def employerProfileView(request):
    return render(request, "employer/profile.html")

def employerCreateView(request):
    return render(request, 'employer/createlisting.html')

def addListing(request):
    
    status = request.POST.get("status")
    job_title = request.POST.get("job_title")
    city = request.POST.get("city")
    description = request.POST.get("")
    organization = request.POST.get("organization")
    contract = request.POST.get("contract")

    addList = Listing(status=status, job_title=job_title, city=city, description = description, organization = organization, contract=contract)
    addList.save()

def editListing(request):

    id = ''
    listing = Listing.objects.get(id = id)
    listing.job_title = request.POST.get('job_title')
    listing.status = request.POST.get("status")
    listing.job_title = request.POST.get("job_title")
    listing.city = request.POST.get("city")
    listing.description = request.POST.get("")
    listing.organization = request.POST.get("organization")
    listing.contract = request.POST.get("contract")

    listing.save()
    return redirect('listing')

def deleteListing(request):
    id = ''
    deleteListing = Listing.objects.get(id=id)
    deleteListing.delete()

def employerEditView(request):
    return render(request, "employer/editlisting.html")


