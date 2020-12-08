from login.views import employerSignUpView
from os import name
from django.urls import path
from .views import editListing, createListing, addOrganization, editEmployerProfile, employerPageView, employerSkillView, employerProfileView, employerCreateView, employerEditView, employerEditProfileView, suggestApp

urlpatterns = [
    path('skills/', employerSkillView, name='skills'),
    path('editprofile/', employerEditProfileView, name='profile'),
    path('profile/', employerProfileView, name='profileView'),
    path('createlisting/', employerCreateView, name='createListing'),
    path('createListingFunc', createListing, name='createListingFunc'),
    path('editlistingview/', employerEditView, name='editListingView'),
    path('edit/listing/', editListing, name='editListing'),
    path('addOrganization/', addOrganization, name='addOrganization'),
    path('profile/edit/', editEmployerProfile, name= 'editProfile'),
    path('suggestListings/<listingid>', suggestApp, name= 'suggestApp'),
    path('', employerPageView, name='employer'),
]
