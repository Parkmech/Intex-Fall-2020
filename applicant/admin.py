from django.contrib import admin
from .models import Applicant, ApplicantSkill, Skill, Organization, Listing, Contract, SavedListing, Application, Offer, PreferredSkill

admin.site.register(Applicant)
admin.site.register(ApplicantSkill)
admin.site.register(Skill)
admin.site.register(Organization)
admin.site.register(Listing)
admin.site.register(Contract)
admin.site.register(SavedListing)
admin.site.register(Application)
admin.site.register(Offer)
admin.site.register(PreferredSkill)


# Register your models here.
