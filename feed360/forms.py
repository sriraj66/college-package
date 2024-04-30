from django import forms
from .models import Questions,FIELD_TYPE

class QuestionsForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.form = kwargs.pop('form', None)
        super(QuestionsForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(QuestionsForm, self).save(commit=False)
        instance.staff = self.user
        instance.form_id = self.form
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Questions
        fields = ['question','field_type']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom:5px;'}),
            'field_type': forms.Select(choices=FIELD_TYPE,attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; padding: 5px;'}),
            }
