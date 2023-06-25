from django.forms import ModelForm, TextInput

from .models import *

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            "text": TextInput(attrs={"placeholder": 'Your Comment'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
