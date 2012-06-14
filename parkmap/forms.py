from django import forms
from models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('park','objectionable_content')
        widgets = dict(rating=forms.RadioSelect())
