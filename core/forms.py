from django import forms
from .models import ChatBot

class CollegeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CollegeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CollegeForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = ChatBot
        fields = ['college', 'name', 'desc', 'logo', 'root_url', 'aditional_urls', 'hints']
        widgets = {
            'college': forms.Select(attrs={'class': 'form-control', 'style': 'margin-bottom:5px;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'logo': forms.URLInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'root_url': forms.URLInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'aditional_urls': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;', 'placeholder': "Enter list of urls by line by line"}),
            'hints': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;'}),
        }
