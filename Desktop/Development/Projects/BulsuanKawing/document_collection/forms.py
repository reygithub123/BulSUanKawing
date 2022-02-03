from django.forms import ModelForm
from django import forms
from document_collection.models import *

class UploadFileForm(ModelForm):
    class Meta:
        model = Document
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'required':True,
                                           'multiple':True, 
                                           'class':'generalfileupload  align-self-end smallfontbtn',
                                           'accept': '.xlsx,.xls,image/*,.doc, .docx,.ppt, .pptx,.txt,.pdf'
                                           }),
        }