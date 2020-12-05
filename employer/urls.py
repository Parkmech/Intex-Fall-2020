from os import name
from django.urls import path
from .views import employerPageView, employerSkillView, employerProfileView, employerCreateView, employerEditView

urlpatterns = [
    path('', employerPageView, name='employer'),
    path('skills/', employerSkillView, name='skills'),
    path('profile/', employerProfileView, name='profile'),
    path('createlisting/', employerCreateView, name='employer'),
    path('editlisting/', employerEditView, name='employer'),
]
