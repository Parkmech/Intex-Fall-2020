from os import name
from django.urls import path
from .views import addProfile, applicantPageView, \
    createScore, editProfile, resumePageView, saveListing, skillsPageView, profilePageView,\
    createScore, scoreListings, searchListings, addProfile, addSkills, \
        deleteSkills, savedListingsPageView, unsaveListing, profileEditPageView, applicationView, applyToJob, \
            aboutPageView, aboutInPageView, deleteApplication, downloadProfileResume, salaryRandom

urlpatterns = [
    path('resume/', resumePageView, name='resume'),
    path('skills/', skillsPageView, name='appSkills'),
    path('skills/add', addSkills, name='addSkills'),
    path('profile/edit', editProfile, name='editAppProfile'),
    path('skills/delete', deleteSkills,name= 'deleteSkills'),
    path('editprofile/', profileEditPageView, name='appProfile'),
    path('profile/download', downloadProfileResume, name='downloadProfileResume'),
    path('profile/', profilePageView, name='appProfileView'),
    path('search/', searchListings, name='applicantSearch'),
    path('addProfile/', addProfile, name='addProfile'),  
    path('savelisting/', saveListing, name='saveListing'),
    path('savedListings/unsaveListing', unsaveListing, name='unsaveListing'),
    path('savedListings', savedListingsPageView, name='savedListings'),
    path('application/delete', deleteApplication, name='deleteApplication'),
    path('application/', applicationView, name='application'),
    path('apply/', applyToJob, name='applyToJob'),
    path('about/', aboutPageView, name='about'),
    path('aboutin/', aboutInPageView, name='aboutin'),
    path('', applicantPageView, name='applicant'),
    path('salaryRandom/', salaryRandom, name='salaryRandom'),
]
