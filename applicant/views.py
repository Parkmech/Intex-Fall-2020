from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Applicant, ApplicantSkill, Organization, PreferredSkill, Listing, Skill

#This function gets the max values for n values in a dictionary
def getMax(dict):

    best_applicants = []
    NUM_APPLICANTS = 10  #This is the number of applicants we want to recommend
    if len(dict) < NUM_APPLICANTS:
        for i in range (0, len(dict)):
            key_max = max(dict, key=dict.get)
            print(dict[key_max])
            best_applicants.append(key_max)
            del dict[key_max]
    else:
        for i in range (0, NUM_APPLICANTS):
            key_max = max(dict, key=dict.get)
            print(dict[key_max])
            best_applicants.append(key_max)
            del dict[key_max]
    print(best_applicants)
    return best_applicants

def listingScore(listing_dict, app_skill_dict):

    counter = 0

    applicant_skills = app_skill_dict.keys() #This is a list containing the Skill_ids of the preferred skills for example preferred_ids = [40,41,42,200]
    listing_scores = {}  #This is a dictionary storing each user and their overall score
    for listing_id, listing_skills in listing_dict.items():
        #(key,value) #value = {40:1, 41:1, ...}, key = 4 (applicantID)
        # print('------------LISTING ID----------------')
        # print(listing_id)
        # print('------------LISTING SKILLS----------------')
        # print(listing_skills)

        for skill in listing_skills: 
            # print('-----------SKILL---------------')
            # print(skill)

            if skill in applicant_skills: #If the skill id is in the applicants skill dictionary (value) then create a score
                listing_skill_level = listing_skills[skill]
            
                if app_skill_dict[skill] > 4: #We only want skills ranging from 0-4, truncate any skills greater than 4 to a value of 4
                    app_skill_dict[skill] = 4

                applicant_skill_level = app_skill_dict[skill]  #preferred skill level
                #Create a score either + or -
                #An applicant with a higher level than preferred gets positive points
                #While applicants with a lower level than preferred gets negative points

                if (applicant_skill_level - listing_skill_level) > 1:
                    listing_score = (listing_skill_level - applicant_skill_level) + 1
                else:
                    listing_score = applicant_skill_level - listing_skill_level

                #Add the score to the user_scores dictionary.
                #This will store each applicant with their overall score for the listing
                if listing_id not in listing_scores:
                    listing_scores[listing_id] = listing_score
                else:
                    listing_scores[listing_id] += listing_score

            else:
                listing_scores[listing_id] -= listing_skills[skill]
                print('---------------------------------')
                print('HERE')
                print('---------------------------------')
        # if counter > 30:
        #     break
        # else:
        #     print('------------COUNTER---------------')
        #     counter += 1
    # print(user_scores)
    return(listing_scores)

#This function returns a score for an applicant base upon the skills 
#asked for by a listing
def applicantScore(applicant_dict, preferred_dict):

    preferred_ids = preferred_dict.keys() #This is a list containing the Skill_ids of the preferred skills for example preferred_ids = [40,41,42,200]
    user_scores = {}  #This is a dictionary storing each user and their overall score
    for key, value in applicant_dict.items():
        #(key,value) #value = {40:1, 41:1, ...}, key = 4 (applicantID)
        for id in preferred_ids:
            
            if id in value: #If the skill id is in the applicants skill dictionary (value) then create a score
                user_level = value[id]
            
                if user_level > 4: #We only want skills ranging from 0-4, truncate any skills greater than 4 to a value of 4
                    user_level = 4

                preferred_level = preferred_dict[id]  #preferred skill level
                #Create a score either + or -
                #An applicant with a higher level than preferred gets positive points
                #While applicants with a lower level than preferred gets negative points
                user_score = user_level - preferred_level

                #Add the score to the user_scores dictionary.
                #This will store each applicant with their overall score for the listing
                if key not in user_scores:
                    user_scores[key] = user_score
                else:
                    user_scores[key] += user_score
    # print(user_scores)
    return(user_scores)

    
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

def searchListings(request):
    search = request.POST.get('search').lower()
    print('-----------',search)
    results = []
    for org in Organization.objects.filter(company_name__icontains=search):
        for listing in Listing.objects.filter(organization=org):
            if listing not in results:
                results.append(listing)
                print('-----ORG------',listing.organization)
    for listing in Listing.objects.filter(job_title__icontains=search, status='published'):
        if listing not in results:
            results.append(listing)
    for listing in Listing.objects.filter(description__icontains=search, status='published'):
        if listing not in results:
            results.append(listing)
    
    skills = PreferredSkill.objects.all()
    print(len(results))
    context = {
        'listings' : results
    }
    return redirect('applicant')


def addProfile(request):

    print('------------------PROFILE INFORMATION-----------------------\n')
    
    print('----------------EMAIL------------------\n')
    email = request.POST.get("email")
    print(email, '\n')
    
    print('----------------USERNAME------------------')
    
    username = request.POST.get("username")

    print(username, '\n')
    print('----------------FIRSTNAME------------------')
    first_name = request.POST.get("first_name")

    print(first_name, '\n')
    print('----------------LASTNAME------------------')
    last_name = request.POST.get("last_name")
    print(last_name, '\n')
    print('----------------PASSWORD------------------')
    password = request.POST.get("password")
    print(password, '\n')

    print('----------------LATEST ID--------------------')
    print(Applicant.objects.latest('id').id)




    app = Applicant(id = Applicant.objects.latest('id').id + 1, email=email, username=username, first_name = first_name, last_name=last_name, password='password')
    app.save()

    
    return redirect("appSkills")


def editProfile(request):
    id = ''
    editApp = Applicant.objects.get(id=id)
    editApp.email = request.get.post("email")
    editApp.username = request.get.post("username")
    editApp.first_name = request.get.post("first_name")
    editApp.password = request.get.post("password")
    
    editApp.save()
    return redirect("profile")

    
def skillsPageView(request):
    app_id = 2
    s = ApplicantSkill.objects.all()
    skills = []
    for i in s:
        if i.applicant.id == app_id:
            skills.append(i)
    print(len(skills))
    context = {
        'skills' : skills
    }
    return render(request, "applicant/skills.html", context)

def addSkills (request) :
    
    skill_id = request.get.post("skill")
    user_id = ''
    level = request.get.post("level")
    appSkill = ApplicantSkill(level=level, user_id=user_id, skill_id=skill_id)
    appSkill.save()
    return redirect("skills")

def deleteSkills (request) :
    
    id= ''
    deleteSkills = ApplicantSkill.objects.get(id=id)
    deleteSkills.delete()

def resumePageView(request):
    return render(request, "applicant/resume.html")

def profilePageView(request):
    return render(request, "applicant/profile.html")

def createScore(request): #Add the listingId as a parameter
    specific_listing_id = 172
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
    top_applicants = getMax(user_scores)

    output = ''
    for i, applicant in enumerate(top_applicants):
        output += f'#{i+1} ApplicantID: ' + str(applicant) + '<br>'
    return HttpResponse(output)

def scoreListings(request):
    specific_applicant_id = 50
    ids = []
    applicant_skills = ApplicantSkill.objects.filter(applicant_id = specific_applicant_id)
    for skill in applicant_skills:
       ids.append(skill.skill_id) #Add the skills of the applicant to the ids list
    
    #Generate the matching skill level for each skill  
    app_skills_dict = {}
    for id in ids:
        if id not in app_skills_dict:
            try:
                app_skills_dict[id] = ApplicantSkill.objects.get(applicant = specific_applicant_id, skill = id).skill_level
            except:
                skills = ApplicantSkill.objects.filter(applicant = specific_applicant_id, skill = id)
                app_skills_dict[id] = skills[0].skill_level
    
    #Create a list with all the listings that have each individual skill
    listing_groups = []
    for id in ids:
        listing_groups.append(PreferredSkill.objects.filter(skill = id))

    #Go through each group and find all of the matching skills for each applicant
    #and put them into a dictionary
    listings = {}
    for listing_group in listing_groups:
        for listing_skill in listing_group: 
            if listing_skill.listing.id not in listings:
                listings[listing_skill.listing.id] = {}
                listings[listing_skill.listing.id][listing_skill.skill.id] = listing_skill.skill_level
            else:
                listings[listing_skill.listing.id][listing_skill.skill.id] = listing_skill.skill_level
    user_scores = listingScore(listings, app_skills_dict)
    top_listings = getMax(user_scores)
    output = ''
    for i, listing in enumerate(top_listings):
        output += f'#{i+1} ListingID: ' + str(listing) + '<br>'
    return HttpResponse(output)