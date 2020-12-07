from os import name
from django.urls import path
from .views import addProfile, applicantPageView, createScore, resumePageView, skillsPageView, profilePageView, createScore, scoreListings, searchListings, addProfile

urlpatterns = [
    path('resume/', resumePageView, name='resume'),
    path('skills/', skillsPageView, name='appSkills'),
    path('profile/', profilePageView, name='profile'),
    path('search/', searchListings, name='applicantSearch'),
    path('addProfile/', addProfile, name='addProfile'),
    path('test/', createScore, name='test'),  #delete later
    path('test2/', scoreListings, name='test2'),  #delete later
    path('', applicantPageView, name='applicant'),
]
