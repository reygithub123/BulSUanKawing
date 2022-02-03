from django.db import models
from django.db.models.fields import CharField, DecimalField
from organization.models import Organization
from images.models import ImageCollection
from django.urls import reverse


class EventState(models.Model):
    status = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return str(self.status)

class Event(models.Model):
    src_ID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()
    description = models.TextField(blank=True)
    img_ID = models.ForeignKey(
        ImageCollection, on_delete=models.CASCADE, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(EventState, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.title) + " from " + str(self.src_ID)

    @property
    def get_html_url(self):
        url = reverse('landing:view-oso-event-desc', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    @property
    def get_org_view_event_html(self):
        url = reverse('landing:view-event-desc', args=(self.src_ID_id,self.id,))
        return f'<a href="{url}" id = {self.id}> {self.title} </a>'
    @property
    def get_event_edit_link(self):
        url = reverse ('org:view-edit-event', args=(self.id,))
        return f'<a href="{url}" id = {self.id}> {self.title} </a>'
    @property
    def get_cms_edit_link(self):
        url = reverse ('cms:view-edit-event', args=(self.id,))
        return f'<a href="{url}" id = {self.id}> ({self.src_ID.acronym}) {self.title} </a>'