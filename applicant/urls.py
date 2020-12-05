from os import name
from django.urls import path
from .views import applicantPageView, resumePageView, skillsPageView, profilePageView

urlpatterns = [
    path('resume/', resumePageView, name='resume'),
    path('skills/', skillsPageView, name='skills'),
    path('profile/', profilePageView, name='profile'),
    path('', applicantPageView, name='applicant'),
]
