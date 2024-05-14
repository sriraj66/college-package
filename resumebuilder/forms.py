from django import forms
from .models import Resume,Socials,Languages

class ResumeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ResumeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ResumeForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Resume
        fields = ['img', 'role', 'bio']
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-bottom:5px;'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;', 'placeholder': "Eg., Frontend Developer"}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'style': 'margin-bottom: 10px; padding: 5px;'}),
        }

class SocialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.res = kwargs.pop('resume', None)
        super(SocialForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(SocialForm, self).save(commit=False)
        instance.res = self.res
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Socials
        fields = ['name', 'url']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select', 'style': 'margin-bottom:5px;'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;', 'placeholder': "Profile URL"}),
        }

class LangForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.res = kwargs.pop('resume', None)
        super(LangForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(LangForm, self).save(commit=False)
        instance.res = self.res
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Languages
        fields = ['name', 'fluency']
        widgets = {
            'fluency': forms.Select(attrs={'class': 'form-select', 'style': 'margin-bottom:5px;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;', 'placeholder': "Eg ., Tamil"}),
        }
    