from applicant.views import scoreListings
from login.views import getEmployerInfo
from login.views import getEmployerInfo
from applicant.models import Contract, PreferredSkill
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from applicant.models import Applicant, ApplicantSkill, PreferredSkill, Listing, Skill, Organization, Application
# Create your views here.

def getMax(dict):

    best_applicants = []
    scores = []
    NUM_APPLICANTS = 12  #This is the number of applicants we want to recommend
    if len(dict) < NUM_APPLICANTS:
        for i in range (0, len(dict)):
            key_max = max(dict, key=dict.get)
            score = dict[key_max]
            scores.append(score)
            best_applicants.append(key_max)
            del dict[key_max]
    else:
        for i in range (0, NUM_APPLICANTS):
            key_max = max(dict, key=dict.get)
            score = dict[key_max]
            scores.append(score)
            best_applicants.append(key_max)
            del dict[key_max]
    # file = open('recommended.txt', 'w')
    # file.write(str(best_applicants))
    # file.close()
    return (best_applicants, scores)

def applicantScore(applicant_dict, preferred_dict):
    counter = 0
    preferred_ids = preferred_dict.keys() #This is a list containing the Skill_ids of the preferred skills for example preferred_ids = [40,41,42,200]
    user_scores = {}  #This is a dictionary storing each user and their overall score
    for key, value in applicant_dict.items():
        #(key,value) #value = {40:1, 41:1, ...}, key = 4 (applicantID)
        for id in preferred_ids:
            
            if id in value: #If the skill id is in the applicants skill dictionary (value) then create a score
                user_level = value[id]
                print('-----------------------------------------')
                print('USER:', key, 'SKILLS:', value, 'CURRENT SKILL', id)
                if user_level > 4: #We only want skills ranging from 0-4, truncate any skills greater than 4 to a value of 4
                    user_level = 4

                preferred_level = preferred_dict[id]  #preferred skill level
                #Create a score either + or -
                #An applicant with a higher level than preferred gets positive points
                #While applicants with a lower level than preferred gets negative points
                user_score = user_level - preferred_level

                #Add the score to the user_scores dictionary.
                #This will store each applicant with their overall score for the listing
                if (user_level - preferred_level) >= 2:
                    print("HIGHER USER LEVEL: Id = ", id, 'preferred level ', preferred_level, 'user level', user_level)
                    if key not in user_scores:
                        user_scores[key] = ((user_level - preferred_level) * -1) + 1
                    else:
                        user_scores[key] += ((user_level - preferred_level) * -1) + 1
                    print('SCORE: ',user_scores[key])

                else:
                    print('HAS SKILL: Id = ', id, 'preferred level ', preferred_level, 'user level ', user_level)
                    if key not in user_scores:
                        user_scores[key] = user_score
                    else:
                        user_scores[key] += user_score
                    print('SCORE: ',user_scores[key])
            else:    
                print('DOESNT HAVE SKILL: Id = ', id, 'preferred level ', preferred_dict[id])
                if key not in user_scores:
                    user_scores[key] = (((preferred_dict[id]) * -1) - 1)
                else:
                    user_scores[key] += (((preferred_dict[id]) * -1) - 1)
                print('SCORE: ',user_scores[key])
        print('USER SCORE:',user_scores[key])
        print('-----------------------------------------', '\n\n\n')
    # print(user_scores)
    return(user_scores)

def createScore(listing_id): #Add the listingId as a parameter
    specific_listing_id = listing_id
    #add the preferred skill ID's to the ids list. This will 
    #be used to query the matching applicants
    ids = []
    preferred_skills = PreferredSkill.objects.filter(listing_id = specific_listing_id) #this will be the dynamically added listing ID 
    for skill in preferred_skills:
       ids.append(skill.skill_id)
    
    #Generate the matching skill level for each skill  
    preferred_dict = {}
    for id in ids:
        preferred_dict[id] = PreferredSkill.objects.get(listing_id = specific_listing_id, skill_id = id).skill_level
    
    #Create a list with all the applicants that have each individual skill
    applicant_groups = []
    for id in ids:
        applicant_groups.append(ApplicantSkill.objects.filter(skill_id = id))

    #Go through each group and find all of the matching skills for each applicant
    #and put them into a dictionary
    applicants = {}
    for applicant_group in applicant_groups:
        for applicant_skill in applicant_group: 
            if applicant_skill.applicant.id not in applicants:
                applicants[applicant_skill.applicant.id] = {}
                applicants[applicant_skill.applicant.id][applicant_skill.skill.id] = applicant_skill.skill_level
            else:
                applicants[applicant_skill.applicant.id][applicant_skill.skill.id] = applicant_skill.skill_level
    user_scores = applicantScore(applicants, preferred_dict)
    top_applicants, top_scores = getMax(user_scores)

    return top_applicants, top_scores

def addOrganization(request):
    
    company_name = request.POST.get("companyName") 
    email = request.POST.get("empEmail")
    password = request.POST.get("empPassword")
    address = request.POST.get("empAddress")
    size = request.POST.get("empSize")
    sector = request.POST.get("empSector")

    org = Organization(company_name = company_name, email = email, password = password, address = address, size=size, sector=sector)
    org.save()

    return redirect("employer")

def employerPageView(request):
    user = getEmployerInfo()
    employer = Organization.objects.get(id=user)
    listings = Listing.objects.filter(organization = employer)
    
    skills = ApplicantSkill.objects.all()
    
    context = {
        'listings' : listings,
        'skills' : skills,
        'employer' : employer
    }
    return render(request, "employer/landing.html", context)

def suggestApp(request, listingid):
    listing = Listing.objects.get(id=listingid)
    applicants = []
    applicantids, appScores = createScore(listingid)
    
    appDict = {}
    for i, applicant in enumerate(applicantids):
        appDict[applicant] = appScores[i]
            
    for aid in applicantids:
        applicants.append(Applicant.objects.get(id=aid))

    skills = ApplicantSkill.objects.all()
    appDictKeys = appDict.keys()

    preferredSkills = PreferredSkill.objects.filter(listing=listing)

    context = {
        'listing' : listing,
        'applicants' : applicants,
        'scores': appScores,
        'skills' : skills,
        'appDict' : appDict,
        'addDictKeys': appDictKeys,
        'preferredSkills' : preferredSkills
    }
    return render(request, "employer/suggestedApplicants.html",context)


def employerSkillView(request,listingid):
    listing = Listing.objects.get(id=listingid)
    preferredSkills = PreferredSkill.objects.filter(listing=listing)
    skills_list = Skill.objects.all()
    
    context = {
        'skills' : preferredSkills,
        'skills_list' : skills_list,
        'listing' : listing
    }
    return render(request, "employer/skills.html", context)

def addPreferredSkills (request) :
    print('--------id--------', request.POST.get('listingid'))
    listing = Listing.objects.get(id=request.POST.get('listingid'))
    skill_name = request.POST.get("skill").lower()
    print('--------skill name--------', skill_name)
    skill = Skill.objects.get(name=skill_name)
    level = request.POST.get("level")

    prefSkill = PreferredSkill(skill_level=level, listing=listing, skill=skill)
    prefSkill.save()

    return redirect("skills", listing.id)

def deletePreferredSkills(request):

    listing = Listing.objects.get(id=request.POST.get('listingid'))
    listingid = request.POST.get('listingid')
    skill = Skill.objects.get(name=request.POST.get('skill').lower())
    delPS = PreferredSkill.objects.get(skill=skill, listing=listing)
    delPS.delete()

    return redirect("skills", listingid)


def employerEditProfileView(request):
    user = getEmployerInfo()
    employer = Organization.objects.get(id=user)
    context = {
        'employer' : employer
    }
    return render(request, "employer/profile.html", context)

def employerProfileView(request):
    user = getEmployerInfo()
    employer = Organization.objects.get(id=user)
    context = {
        'employer' : employer
    }
    return render(request, "employer/profileview.html", context)

def editEmployerProfile(request):
    user = getEmployerInfo()
    edit_org = Organization.objects.get(id=user)
    edit_org.company_name = request.POST.get('name')
    edit_org.password = request.POST.get('password')
    edit_org.address = request.POST.get('address')
    edit_org.size = request.POST.get('size')
    edit_org.sector = request.POST.get('sector')
    edit_org.save()
    return redirect("profileView")

def employerCreateView(request):
    return render(request, 'employer/createlisting.html')

def employerAboutView(request):
    return render(request, 'employer/about.html')

def createListing(request):
    
    status = request.POST.get("status")
    job_title = request.POST.get("job_title")
    city = request.POST.get("city")
    description = request.POST.get("description")
    organization = Organization.objects.get(id=getEmployerInfo())
    contract_name = request.POST.get('contract')
    contract = Contract.objects.get(type=contract_name)

    createList = Listing(status=status, job_title=job_title, city=city, description = description, organization = organization, contract=contract)
    createList.save()
    

    return redirect('skills',createList.id)

def editListing(request):
    listingid = request.POST.get('id')
    contract = request.POST.get('contract')
    contract = Contract.objects.get(type=contract)
    #contract = Contract.objects.get(id=listingid)
    organization = Organization.objects.get(id=getEmployerInfo())

    editList = Listing.objects.get(id=listingid)
    
    editList.status = request.POST.get("status")
    editList.job_title = request.POST.get("job_title")
    editList.city = request.POST.get("city")
    editList.description = request.POST.get("description")
    editList.contract = contract
    editList.save()    
    
    return redirect('skills',editList.id)

def deleteListing(request):
    listingid = request.POST.get('listingid')
    deleteListing = Listing.objects.get(id=listingid)
    deleteListing.delete()
    return redirect('employer')

def employerEditView(request):
    listingid = request.POST.get('listingid')
    listing = Listing.objects.get(id=listingid)
    contracts = Contract.objects.all()
    context = {
        'listing' : listing,
        'contracts' : contracts
    }
    return render(request, "employer/editlisting.html", context)


def matchbox(web_request):

    import urllib
    
    # If you are using Python 3+, import urllib instead of urllib2
    import json 

    print('-----------------------------------', 'INPUTS')
    data = {
            "Inputs": {
                    "input1":
                    [
                        {
                                'user_id': web_request.POST.get('applicantid'),      
                        }
                    ],
            },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))
    
    url = 'https://ussouthcentral.services.azureml.net/workspaces/a8edf043f79741ce9a6e68aa93e3270d/services/1dec62180cd34263b1a0027f0100b3b8/execute?api-version=2.0&format=swagger'
    api_key = 'xIwALjzfLRpstOGYQZuIzb4uzi3IvnQdaWBq698VnhahFlWOqYQpZzsagF63FMoJKYZOjxao4GDEWogRFUNSmQ=='
    # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    from  urllib import request
    req = urllib.request.Request(url, body, headers) 
    req.method = "POST"
    response = request.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

    result = response.read()
    result = json.loads(result)
      
    idList = []
    output = '<b>Recommended Users:</b>' + '<br><br>'
    for i in range(0, 12):

        output += f'User {i + 1}: ' + result['Results']['output1'][0]['Related User ' + str(i+1)] + '<br>'
        idList.append(result['Results']['output1'][0]['Related User ' + str(i+1)])
    
    applicants = []
    for aid in idList:
        applicants.append(Applicant.objects.get(id=aid))

    skills = ApplicantSkill.objects.all()
    base_applicant = Applicant.objects.get(id=web_request.POST.get('applicantid'))
    listing = Listing.objects.get(id=web_request.POST.get('listingid'))

    preferredSkills = PreferredSkill.objects.filter(listing=listing)

    context = {
        'applicants' : applicants,
        'skills' : skills,
        'base_applicant' : base_applicant,
        'listing' : listing,
        'preferredSkills' : preferredSkills
    }
    return render(web_request, 'employer/moreUsers.html',context) 
    





    





    





    





    





    





    





    





    




