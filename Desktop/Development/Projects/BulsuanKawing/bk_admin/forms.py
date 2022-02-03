
from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from django.views.decorators.http import last_modified

from announcements.models import *
from events.models import Event
from information.models import *
from organization.models import Organization

class GeneralInformationForm(ModelForm):
    class Meta:
        model = GeneralInformation
        exclude = ['logo']
        widgets ={
            'office_name':forms.TextInput(attrs={'class':'standard-field','placeholder':'Office Name'}),
            'name_acronym':forms.TextInput(attrs={'class':'standard-field','placeholder':'Office Acronym'}),
            'about':forms.Textarea(attrs={'class':'standard-field','placeholder':'Brief Discussion'}),
            'description':forms.Textarea(attrs={'class':'standard-field','placeholder':'What is OSOA?'}),
            'history':forms.Textarea(attrs={'class':'standard-field','placeholder':'History'}),
        }


class ChangeLogoForm(ModelForm):
    class Meta:
        model = GeneralInformation
        fields = ['logo']
        widgets={
            'logo': forms.FileInput(attrs={'class':'upload_image','hidden':True,'id':'actual-btn','onchange':'changeImage(this)'}),
            
        }
        
class EditAccountForm(UserChangeForm):
    class Meta:
        model = User
        USERNAME_FIELD = "email"
        REQUIRED_FIELDS = ["username",'email']
        fields = ['username','email','password']
        widgets={
            'username': forms.TextInput(attrs={'class':'standard-field','placeholder':'Username','required':True}),
            'email': forms.TextInput(attrs={'class':'standard-field','placeholder':'eg. bulsuosoa@bulsuankawing.com','type':'email'})
        }
        
class AddCMSEventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'src_ID':forms.Select(attrs={'class':'standard-field'}),
            'title' :forms.TextInput(attrs={'class':'standard-field'}),
            'description' :forms.Textarea(attrs={'class':'standard-field'}),
            'time_begin': forms.DateInput(attrs={'type': 'datetime-local' ,'class':'standard-field'}, format='%Y-%m-%dT%H:%M'),
            'time_end': forms.DateInput(attrs={'type': 'datetime-local', 'class':'standard-field'}, format='%Y-%m-%dT%H:%M'),
            'state':forms.Select(attrs={'class':'standard-field'}),
        }
        exclude = ('img_ID',)

    def __init__(self, *args, **kwargs):
        super(AddCMSEventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['time_begin'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['time_end'].input_formats = ('%Y-%m-%dT%H:%M',)
class NewsForm(ModelForm):
    class Meta:
        model = Announcement
        widgets ={
            'title':forms.TextInput(attrs={'class':'standard-field'}),
            'description' :forms.Textarea(attrs={'class':'standard-field'}),
            'published':forms.DateInput(attrs={'type': 'datetime-local' ,'class':'standard-field'}, format='%Y-%m-%dT%H:%M'),
        }
        
        exclude = ('img_ID','last_modified')

class OfficerForm(ModelForm):
    class Meta:
        model = Officer
        widgets={
             'name':forms.TextInput(attrs={'class':'standard-field'}),
             'position':forms.TextInput(attrs={'class':'standard-field'}),
             'image':forms.FileInput(attrs={'class':'generalfileupload'}),
             'hierarchy':forms.Select(attrs={'class':'standard-field'}),
             
        }
        fields='__all__'