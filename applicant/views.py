from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Applicant, ApplicantSkill, PreferredSkill, Listing, Skill

# Create your views here.
def applicantPageView(request):
    l = Listing.objects.all()
    listings = []
    for i in l:
        listings.append(i)
    listings = listings[0:20]
    skills = PreferredSkill.objects.all()

        
    
    context = {
        'listings' : listings,
        'skills' : skills
    }
    print('test')
    return render(request, "applicant/landing.html", context)

def skillsPageView(request):
    return render(request, "applicant/skills.html")

def resumePageView(request):
    return render(request, "applicant/resume.html")

def profilePageView(request):
    return render(request, "applicant/profile.html")

def createScore(request): #Add the listingId as a parameter

    ids = []
    preferred_skills = PreferredSkill.objects.filter(listing_id = 44) #this will be the dynamically added listing ID 
    for skill in preferred_skills:
       ids.append(skill.skill_id)
    
    applicant_groups = []
    for id in ids:
        applicant_groups.append(ApplicantSkill.objects.filter(skill_id = id))

    output = ''
    applicants = {}

    for applicant_group in applicant_groups:
        for applicant_skill in applicant_group: 
            if applicant_skill.applicant.id not in applicants:
                applicants[applicant_skill.applicant.id] = {}
                applicants[applicant_skill.applicant.id][applicant_skill.skill.id] = applicant_skill.skill_level
            else:
                applicants[applicant_skill.applicant.id][applicant_skill.skill.id] = applicant_skill.skill_level

    print(applicants)
    return HttpResponse(applicants.values())
    

