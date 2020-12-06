from os import name
from django.urls import path
from .views import applicantPageView, createScore, resumePageView, skillsPageView, profilePageView, createScore

urlpatterns = [
    path('resume/', resumePageView, name='resume'),
    path('skills/', skillsPageView, name='skills'),
    path('profile/', profilePageView, name='profile'),
    path('test/', createScore, name='test'),          #delete this later
    path('', applicantPageView, name='applicant'),
]
