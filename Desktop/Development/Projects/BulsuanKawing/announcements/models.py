from django.db import models
from organization.models import Organization
from images.models import ImageCollection


class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    published = models.DateTimeField()
    description = models.TextField(blank=True)
    img_ID = models.ForeignKey(
        ImageCollection, on_delete=models.CASCADE,  null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
