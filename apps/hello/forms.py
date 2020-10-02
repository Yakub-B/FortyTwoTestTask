from django import forms
from apps.hello.models import ProfileModel


class EditProfileDataForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'
        widgets = {
            'birthday_date': forms.DateInput(attrs={'type': 'date'})
        }
