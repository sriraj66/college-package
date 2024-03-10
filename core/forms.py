from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CollegeForm(forms.ModelForm):
    
    class Meta:
        model = College
        fields = ['name','api_key','desc','logo','root_url','aditional_urls','hints']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'logo': forms.URLInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'root_url': forms.URLInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'aditional_urls': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;','placeholder':"Enter list of urls by line by line"}),
            'hints': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;'}),
        }