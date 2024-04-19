from django import forms
from .models import Students

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['phone', 'gender', 'profile']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;', 'placeholder': " Mobile Number "}),
            'gender': forms.Select(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            'profile': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.setdefault('initial', {})['phone'] = instance.phone
            kwargs.setdefault('initial', {})['gender'] = instance.gender
            kwargs.setdefault('initial', {})['profile'] = instance.profile
        super(StudentProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(StudentProfileForm, self).save(commit=False)
        if commit:
            if instance.phone !=0  and instance.gender != "None":
                instance.is_completed = True
            else:
                instance.is_completed = False
            instance.save()
        return instance
