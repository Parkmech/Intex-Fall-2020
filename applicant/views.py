from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Applicant, ApplicantSkill, Organization, PreferredSkill, Listing, SavedListing, Skill, Application
#from django_globals import globals 
# from login.users import current_user
# from login.users import set_user

#RETURN USER INFO FOR THE SESSION
def getUserInfo():
    file = open('current_user.txt', 'r')
    current_user =  int(file.readline())
    return current_user

#SET USER INFO FOR THE SESSION
def setUserInfo(user_id):
    file = open('current_user.txt', 'w')
    file.write(str(user_id))
    file.close()

#This function gets the max values for n values in a dictionary
def getMax(dict):
    best_applicants = [] #this list will hold the best applicants
    NUM_APPLICANTS = 10  #This is the number of applicants we want to recommend
    if len(dict) < NUM_APPLICANTS: #if there are less items in the dict than the number of applicants to return
        for i in range (0, len(dict)):
            key_max = max(dict, key=dict.get)
            best_applicants.append(key_max)
            del dict[key_max]
    else:
        for i in range (0, NUM_APPLICANTS):
            key_max = max(dict, key=dict.get)
            best_applicants.append(key_max)
            del dict[key_max]
    return best_applicants

def listingScore(listing_dict, app_skill_dict):

    applicant_skills = app_skill_dict.keys() #This is a list containing the Skill_ids of the preferred skills for example preferred_ids = [40,41,42,200]
    listing_scores = {}  #This is a dictionary storing each user and their overall score
    for listing_id, listing_skills in listing_dict.items():
        #(key,value) listing_skills = {40:1, 41:1, ...}, listingID = 4

        for skill in listing_skills: 

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
    return(user_scores)

#RETURN the applicant landing page with the recommended listings for their skill set
def applicantPageView(request):
    user = getUserInfo()
    recommended_listings = scoreListings(user) #[104265, 104766, 100872, 101032, 101101, 101136, 101269, 101291, 101391, 101980]
    listings = []
    for listing in recommended_listings:  
        listings.append(Listing.objects.get(id=listing))
    skills = PreferredSkill.objects.all()
    applicant = Applicant.objects.get(id=user)
    applicant_skills = ApplicantSkill.objects.filter(applicant=applicant)
    context = {
        'listings' : listings,
        'skills' : skills,
        'applicant' : user,
        'applicant_skills' : applicant_skills
    }
    
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

def saveListing(request):
    user = getUserInfo()
    listingid = request.POST.get('id')
    listing = Listing.objects.get(id=listingid)
    applicant = Applicant.objects.get(id=user)
    savedListing = SavedListing(listing = listing, applicant = applicant)
    savedListing.save()
    return redirect('applicant')

def addProfile(request):

    email = request.POST.get("email") 
    username = request.POST.get("username")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    password = request.POST.get("password")

    app = Applicant(email=email, username=username, first_name = first_name, last_name=last_name, password='password')
    app.save()
    
    user = Applicant.objects.get(username = username, password = 'password')
    setUserInfo(user.id)

    return redirect("appSkills")


def editProfile(request):
    user = getUserInfo()
    applicant = Applicant.objects.get(id=user)
    editApp = Applicant.objects.get(id=user)
    editApp.first_name = request.POST.get("appFirst")
    editApp.last_name = request.POST.get("appLast")
    editApp.password = request.POST.get("appPassword")
    editApp.save()

    return redirect("appProfileView")

    
def skillsPageView(request):
    app_id = getUserInfo()
    s = ApplicantSkill.objects.all()
    skills = []
    for i in s:
        if i.applicant.id == app_id:
            skills.append(i)
    dropdown = Skill.objects.all()
    context = {
        'skills' : skills,
        'dropdown' : dropdown
    }
    return render(request, "applicant/skills.html", context)

def addSkills (request) :
    skill = Skill.objects.get(name=request.POST.get('skill').lower())
    level = request.POST.get('level')
    user = Applicant.objects.get(id=getUserInfo())
    appSkill = ApplicantSkill(applicant = user, skill = skill, skill_level = level)
    appSkill.save()
    return redirect("appSkills")

def deleteSkills (request) :
    user = Applicant.objects.get(id=getUserInfo())
    skill = Skill.objects.get(name=request.POST.get('del').lower())
    del_obj = ApplicantSkill.objects.get(applicant = user,skill=skill)
    del_obj.delete()
    return redirect('appSkills')

def resumePageView(request):
    return render(request, "applicant/resume.html")

def profileEditPageView(request):
    user = getUserInfo()
    applicant = Applicant.objects.get(id=user)
    context = {
        'applicant' : applicant
    }
    return render(request, "applicant/profile.html", context)

def profilePageView(request):
    user = getUserInfo()
    applicant = Applicant.objects.get(id=user)
    context = {
        'applicant' : applicant
    }
    return render(request, "applicant/profileview.html",context)

def savedListingsPageView (request):
    userid = getUserInfo()
    user = Applicant.objects.get(id=userid)
    savedListings = SavedListing.objects.filter(applicant=user)
    listings = []
    for sl in savedListings:
        listings.append(Listing.objects.get(id=sl.listing.id))
    skills = PreferredSkill.objects.all()

    context = {
        'listings' : listings,
        'skills' : skills
    }
    return render(request, "applicant/savedlistings.html", context)

def unsaveListing(request):
    userid = getUserInfo()
    applicant = Applicant.objects.get(id=userid)
    listingid = request.POST.get('listingid')
    listing = Listing.objects.get(id=listingid)
    del_sl = SavedListing.objects.get(listing=listing,applicant=applicant)
    del_sl.delete()
    return redirect('savedListings')

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
    top_applicants = getMax(user_scores)
    return top_applicants

def applicationView(request):
    user = getUserInfo()
    applicant = Applicant.objects.get(id=user)

    applications = Application.objects.filter(applicant=applicant)

    listing = Listing.objects.get(id=user)
     
    context = {
        'applications' : applications,
        'applicant' : applicant,
        'listing' : listing,

    }
    return render(request, "applicant/application.html", context)

def deleteApplication(request):
    application = Application.objects.get(id=request.POST.get('id'))
    application.delete()
    return redirect('application')


def scoreListings(user):
    specific_applicant_id = 100050
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
    return top_listings
    # return HttpResponse(output)

def applyToJob (request):

    listing = Listing.objects.get(id=getUserInfo())
    applicant = Applicant.objects.get(id=getUserInfo())
    status = 'Pending'
    matchingSkills = 0
    
    application = Application(listing = listing, applicant = applicant, status=status, matching_skills = matchingSkills)

    application.save()
    
    return redirect("application")

def aboutPageView (request):
    return render(request, 'applicant/about.html')

def aboutInPageView (request):
    return render(request, 'applicant/aboutin.html')