from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.models import ModelForm
from django.forms.widgets import DateInput

from .models import *
from colorfield.fields import ColorField

class WorkForm(forms.Form):
    name = forms.CharField(max_length=60,label="", widget=forms.TextInput(attrs={'name': 'name', 'class': 'inpclear inpf ', 'class': 'standard-field', 'placeholder':'eg. BALANGAYAN Tasks' }))
    order = forms.DecimalField(widget=forms.NumberInput(attrs={'min':'1', 'max':'100', 'class': 'inpclear inpf inputnumber', 'class': 'standard-number-field', }), max_digits=100, validators=[MinValueValidator(1), MaxValueValidator(100)])
    color = forms.CharField(label='Color', max_length=7,
        widget=forms.TextInput(attrs={'type': 'color', 'value':'#ffd700',  'class': 'standard-color-field'}))
     
class TaskForm(ModelForm):
    class Meta:
            model = Task
            fields = ['tdl_ID','name','description','time_begin', 'time_end']
            widgets = {
                'name':forms.TextInput(attrs={'id':'task_name', 'class': 'standard-field', 'placeholder':'eg. Set Up Event'}),
                'description' :forms.Textarea(attrs={ 'class': 'standard-field'}),
                'time_begin': DateInput(attrs={'type': 'datetime-local', 'class': 'standard-field'}, format='%Y-%m-%dT%H:%M'),
                'time_end': DateInput(attrs={'type': 'datetime-local', 'class': 'standard-field'}, format='%Y-%m-%dT%H:%M'),
            }
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['time_begin'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['time_end'].input_formats = ('%Y-%m-%dT%H:%M',)

