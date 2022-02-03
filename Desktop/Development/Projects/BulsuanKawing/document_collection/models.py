from django.db import models
from organization.models import Organization
from datetime import date
from events.models import Event, EventState


class Category (models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
    
class DocumentCollection (models.Model):
    
    src_ID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    submitted = models.DateTimeField(auto_now=True)
    message = models.TextField( null=True, blank=True)
    state = models.ForeignKey(EventState, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.name) + " from " + str(self.src_ID.acronym)


class Document (models.Model):

    collection = models.ForeignKey(
        DocumentCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True, default="")
    state = models.ForeignKey(EventState, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(
        upload_to='documents/', blank=False, null=False)
    def __str__(self):
        return str(self.name) + " from " + str(self.collection.name)