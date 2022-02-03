from django.forms import ModelForm, forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import HiddenInput
from organization.models import Organization

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        USERNAME_FIELD = "email"
        REQUIRED_FIELDS = ["username"]
        fields = ['username', 'email', 'password1', 'password2']

class InitializeOrgForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['user','state']
        widgets = {
            'user': forms.HiddenInput,
            'state': forms.HiddenInput,
        }

class EditOrgForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ['user', 'state', 'program', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class':'orgsetuptxtfield'}),
            'acronym': forms.TextInput(attrs={'class':'orgsetuptxtfield'}),
            'num_of_members': forms.NumberInput(attrs={'min':'1','class':'orgsetuptxtfield'}),
            'year_established': forms.NumberInput(attrs={'min':'1990', 'max':'2050','class':'orgsetuptxtfield'}),
            'by_laws_src': forms.FileInput(attrs={'class':'upload_file','hidden':True, 'id':'bylaws-btn'}),
            'logo': forms.FileInput(attrs={'class':'upload_image','hidden':True,'id':'actual-btn','onchange':'changeImage(this)','accept': 'image/*'}),
            
        }
        

class EditSettingOrgForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ['user', 'state','by_laws_src','logo', 'program', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class':' standard-field', 'placeholder':'Name'}),
            'acronym': forms.TextInput(attrs={'class':' standard-field', 'placeholder':'Acronym'}),
            'num_of_members': forms.NumberInput(attrs={'min':'1','class':' standard-field', 'placeholder':'Number of Members'}),
            'year_established': forms.NumberInput(attrs={'min':'1990', 'max':'2050','class':'standard-field', 'placeholder':'Year Founded'}),

        }
class UploadLogoForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['logo']
        widgets = {
            'logo': forms.FileInput(attrs={'class':'upload_image','hidden':True,'id':'actual-btn','onchange':'changeImage(this)'}),
        }
        
class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        REQUIRED_FIELDS = ["username", "email"]
        fields = ['username', 'email']
        widgets = {
            'username':  forms.TextInput(attrs={'class':'standard-field', 'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'class':'standard-field','type':'email', 'placeholder':'E-Mail', 'required':True},)
        }
        
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'standard-field', 'type':'password'}))
    new_password1 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'standard-field', 'type':'password'}))
    new_password2 = forms.CharField(widget = forms.PasswordInput(attrs={'class':'standard-field', 'type':'password'}))
    
