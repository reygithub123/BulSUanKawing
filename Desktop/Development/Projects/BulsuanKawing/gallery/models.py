from django.db import models
from django.utils import timezone
from organization.models import Organization
  

class Album (models.Model):
    src_ID = models.ForeignKey(Organization, on_delete=models.CASCADE ,blank=False, null=False, default =0)
    name = models.CharField(max_length=100, null=False, blank=False, default="")
    key_image = models.ImageField(
        upload_to='imageresources/', default ="")
    last_modified = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now=True)
    
    admin = models.BooleanField(default=False, blank=False, null=False)
    def __str__(self):
        return str(self.src_ID.acronym) + ": " + str(self.name)

class Image(models.Model):
    
    album = models.ForeignKey(Album, on_delete = models.CASCADE)
    
    image =  models.ImageField(
        upload_to='imageresources/', blank=False, null=False)
    
    name = models.CharField(max_length=100, blank = True, null = False, default = "")
    
    last_modified = models.DateTimeField(default=timezone.now)
    
    uploaded = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.album.name)+": "+str(self.name) +" ("+ str(self.album.src_ID.acronym)+") Image"

    class Meta:
        verbose_name_plural = "Images"
