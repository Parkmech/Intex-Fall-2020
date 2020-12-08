from os import name
from django.urls import path
from .views import addProfile, applicantPageView, \
    createScore, editProfile, resumePageView, saveListing, skillsPageView, profilePageView,\
    createScore, scoreListings, searchListings, addProfile, addSkills, \
        deleteSkills, savedListingsPageView, unsaveListing, profileEditPageView, applicationView

urlpatterns = [
    path('resume/', resumePageView, name='resume'),
    path('skills/', skillsPageView, name='appSkills'),
    path('skills/add', addSkills, name='addSkills'),
    path('profile/edit', editProfile, name='editAppProfile'),
    path('skills/delete', deleteSkills,name= 'deleteSkills'),
    path('editprofile/', profileEditPageView, name='appProfile'),
    path('profile/', profilePageView, name='appProfileView'),
    path('search/', searchListings, name='applicantSearch'),
    path('addProfile/', addProfile, name='addProfile'),  
    path('savelisting/', saveListing, name='saveListing'),
    path('savedListings/unsaveListing', unsaveListing, name='unsaveListing'),
    path('savedListings', savedListingsPageView, name='savedListings'),
    path('', applicantPageView, name='applicant'),
    path('application/', applicationView, name='application')
]
