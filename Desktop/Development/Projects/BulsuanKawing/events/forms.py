from django.forms import ModelForm, DateInput
from django.forms.widgets import FileInput, TextInput, Textarea
from .models import Event
from images.models import ImageCollection

class AddEventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'title' :TextInput(attrs={'class':'standard-field'}),
            'description' :Textarea(attrs={'class':'standard-field'}),
            'time_begin': DateInput(attrs={'type': 'datetime-local' ,'class':'standard-field'}, format='%Y-%m-%dT%H:%M'),
            'time_end': DateInput(attrs={'type': 'datetime-local', 'class':'standard-field'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('title', 'time_begin', 'time_end', 'description')

    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['time_begin'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['time_end'].input_formats = ('%Y-%m-%dT%H:%M',)

class AddEventImageForm(ModelForm):
    class Meta:
        model = ImageCollection
        
        fields = ('img_src',)
        widgets ={
            'img_src': FileInput(attrs={'class':'generalfileupload', 'onchange':'changeImage(this)'})
        }
        
class EditEventImageForm(ModelForm):
    class Meta:
        model = ImageCollection
        
        fields = ('img_src',)
        widgets ={
            'img_src': FileInput(attrs={'class':'generalfileupload', 'onchange':'changeImage(this)', 'required':False})
        }