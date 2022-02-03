from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

class GeneralInformation(models.Model):
    office_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    name_acronym = models.CharField(max_length=100, null=False, blank=False, default = "BulSU-OSOA")
    about = models.TextField(null=False, blank=False, default = "About BulSU-OSOA")
    description = models.TextField(null=False, blank=False, default = "What is BulSU-OSOA?")
    history = models.TextField(null=False, blank=False, default = "BulSU-OSOA Complete History")
    logo = models.ImageField(upload_to='imageresources/', blank=False, null=False, default = "imageresources/osologo.svg")
    
    def __str__(self): 
            return self.office_name +" General Information"
    class Meta:
        verbose_name_plural = "General Information"
        
class Officer(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    position = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to='executiveboard/', blank=False, null=False, default = "imageresources/osologo.svg")
    
    HIERARCHY_CHOICES = (
            (0,'Head (Head of Office)'),
            (1,'Leaders(Chairman/Vice Chairman)'),
            (2,'Internal/Primary(Executive Board/Committees)'), 
            (3, 'External/Secondary'),
            (4, 'Others')
    )
    hierarchy = models.PositiveIntegerField(choices = HIERARCHY_CHOICES,default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])
    def __str__(self):
            return self.name +" - " + self.position
        
class TypesOfOrganization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = description = models.TextField(null=False, blank=False, default = "Describe Type of Org")
    def __str__(self):
            return self.name
        
    class Meta:
        verbose_name_plural = "Org Types"