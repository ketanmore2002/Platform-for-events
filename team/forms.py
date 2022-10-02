from django import forms

from .models import *

class eventsForm(forms.ModelForm):
    
    class Meta:
        model = events
        fields = "__all__"


class playerForm(forms.ModelForm):
    
    class Meta:
        model = player
        fields = "__all__"


class teamsForm(forms.ModelForm):
    
    class Meta:
        model = teams
        fields = "__all__"
