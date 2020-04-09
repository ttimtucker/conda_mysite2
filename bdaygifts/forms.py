from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from .models import Profile

FILTER_CHOICES = (
    ('OH', 'Ohio'),
    ('World', 'World')
)

#class Region_Form(forms.Form):
#    widget=forms.CharField(label='Select Region',widget=forms.Select(choices=REGION_CHOICES))

class Region_Selected(forms.Form):
    region=forms.CharField(max_length=20)


class FilterForm(forms.Form):
    filter_by = forms.ChoiceField(choices=FILTER_CHOICES)

class PlotForm(forms.Form):
     filter_by = forms.ChoiceField(choices=FILTER_CHOICES)