import datetime
from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone

from colorfield.fields import ColorField
from organization.models import Organization


class Workspace(models.Model):
    src_ID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="Organization Workspace")

    def __str__(self):
        return str(self.src_ID) + " Work Set"


class ToDoList(models.Model):
    wp_ID = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    order = models.DecimalField(decimal_places=0, max_digits=100)
    color = ColorField(default='#00546A')

    def __str__(self):
        return self.name


class TaskState(models.Model):
    name = models.CharField(
        max_length=50, null=False, blank=False, default="todo")
    
    def __str__(self):
        return self.name +"("+str(self.pk)+")"

class Task(models.Model):
    tdl_ID = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True)
    made = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(TaskState, on_delete=models.DO_NOTHING, default = 1)
    def __str__(self):
        return self.name
    @property
    def is_past_due(self):
        past = timezone.now() > self.time_end and self.state.id != 3
        return past
