from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from information.models import TypesOfOrganization

User = get_user_model()

class Program (models.Model):
    name = models.CharField(max_length=150,null=False, blank=False)
    acronym = models.CharField(max_length=50, null=True, blank=True)
    college =models.CharField(max_length=150,null=False, blank=False)
    college_acronym =models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f"({self.acronym}) {self.college_acronym}"
    
class Organization(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150,null=False, blank=False)
    acronym = models.CharField(max_length=50, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    num_of_members = models.DecimalField(decimal_places=0, max_digits=100,default=0,validators=[
            MinValueValidator(0)
        ])
    
    year_established = models.DecimalField(decimal_places=0, max_digits=4, default=1990,validators=[
            MaxValueValidator(2050),
            MinValueValidator(1990)
        ])
    by_laws_src = models.FileField(
        upload_to='documents/', blank=False, null=False, default='')
    
    logo = models.ImageField(
        upload_to='imageresources/', blank=False, null=False, default = '/imageresources/osologo.svg')
    uploaded = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    OSOA = 'o'
    NONE= 'n'
    REGISTERED = 'r'
    PENDING = 'p'
    SETUP = 's'
    CAT_CHOICES = (
        (OSOA, 'OSOA'),
        (NONE, 'none'),
    )
    category = models.ForeignKey(TypesOfOrganization, on_delete=models.SET_NULL, null=True,blank=True)
    
    STATE_CHOICES = (
        (OSOA, 'OSOA'),
        (REGISTERED, 'Registered'),
        (PENDING, 'Pending'),
        (SETUP, 'Setup'),
    )
    state = models.CharField(max_length=20,choices =STATE_CHOICES, default ="Setup" )

    def __str__(self):
        return f"{self.name} ({self.acronym})"
