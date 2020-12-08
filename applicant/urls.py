from os import name
from django.urls import path
from .views import addProfile, applicantPageView, \
    createScore, resumePageView, saveListing, skillsPageView, profilePageView,\
    createScore, scoreListings, searchListings, addProfile, addSkills, \
        deleteSkills, savedListingsPageView, unsaveListing

urlpatterns = [
    path('resume/', resumePageView, name='resume'),
    path('skills/', skillsPageView, name='appSkills'),
    path('skills/add', addSkills, name='addSkills'),
    path('skills/delete', deleteSkills,name= 'deleteSkills'),
    path('profile/', profilePageView, name='appProfile'),
    path('search/', searchListings, name='applicantSearch'),
    path('addProfile/', addProfile, name='addProfile'),
    # path('appSignin/', appSignin, name='appSignin'),
        
    path('savelisting/', saveListing, name='saveListing'),
    path('savedListings/unsaveListing', unsaveListing, name='unsaveListing'),
    path('savedListings', savedListingsPageView, name='savedListings'),
    path('', applicantPageView, name='applicant'),
]
