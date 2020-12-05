from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator, integer_validator
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Applicant(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    #resume = models.FileField(upload_to='files')
    #photo = models.ImageField(upload_to = 'photos')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Skill(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class ApplicantSkill(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=CASCADE) 
    skill = models.ForeignKey(Skill, on_delete=CASCADE)
    skill_level = models.IntegerField(default=1,
        validators=[MaxValueValidator(4), MinValueValidator(0)])

    def __str__(self):
        return str(self.applicant) + ' ' + str(self.skill)

class Organization(models.Model):
    company_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    address = models.CharField(max_length=50)
    size = models.CharField(max_length=25)
    sector = models.CharField(max_length=2)
    #photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.company_name
    
class Listing(models.Model) :
    status = models.CharField(max_length=20)
    job_title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    organization = models.ForeignKey(Organization, on_delete=CASCADE)

    def __str__(self):
        return self.job_title
    
class Contract(models.Model) :
    listing = ForeignKey(Listing, on_delete=CASCADE)
    type = models.CharField(max_length=2)

    def __str__(self):
        return str(self.listing) + ' ' + str(self.type)

class SavedListing(models.Model):
    applicant = ForeignKey(Applicant, on_delete=CASCADE)
    listing = ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return str(self.applicant) + ' ' + str(self.listing)

class  Application(models.Model):
    listing = ForeignKey(Listing, on_delete=CASCADE)
    applicant = ForeignKey(Applicant, on_delete=CASCADE)
    status = CharField(max_length=20)
    matching_skills = IntegerField()

    def __str__(self):
        return str(self.listing) + ', ' + str(self.applicant) + "'s Application" 

class Offer(models.Model):
    text = models.CharField(max_length=1000)
    application = models.ForeignKey(Application, on_delete=CASCADE)

    def __str__(self):
        return self.text

class PreferredSkill(models.Model):
    skill = ForeignKey(Skill, on_delete=CASCADE)
    listing = ForeignKey(Listing, on_delete=CASCADE)
    skill_level = models.IntegerField(default=1,
        validators=[MaxValueValidator(4),MinValueValidator(0)])

    def __str__(self):
        return str(self.listing) + ', ' + str(self.skill)  + ' ' + str(self.skill_level) 