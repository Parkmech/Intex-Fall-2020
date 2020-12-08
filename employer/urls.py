from login.views import employerSignUpView
from os import name
from django.urls import path
from .views import addOrganization, employerPageView, employerSkillView, employerProfileView, employerCreateView, employerEditView

urlpatterns = [
    path('skills/', employerSkillView, name='skills'),
    path('profile/', employerProfileView, name='profile'),
    path('createlisting/', employerCreateView, name='createListing'),
    path('editlisting/', employerEditView, name='editListing'),
    path('addOrganization/', addOrganization, name='addOrganization'),
    path('', employerPageView, name='employer'),
]
