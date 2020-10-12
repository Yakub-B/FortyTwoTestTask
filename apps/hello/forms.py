from django import forms
from apps.hello.models import ProfileModel


class EditProfileDataForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'v-model': 'name', ':disabled': 'fieldsDisable'}),
            'last_name': forms.TextInput(attrs={'v-model': 'last_name', ':disabled': 'fieldsDisable'}),
            'birthday_date': forms.DateInput(attrs={
                'type': 'date', 'v-model': 'birthday_date', ':disabled': 'fieldsDisable'
            }),
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 24, 'v-model': 'bio', ':disabled': 'fieldsDisable'}),
            'other_contacts': forms.Textarea(attrs={
                'rows': 4, 'cols': 24, 'v-model': 'other_contacts', ':disabled': 'fieldsDisable'
            }),
            'jabber': forms.TextInput(attrs={'v-model': 'jabber', ':disabled': 'fieldsDisable'}),
            'email': forms.EmailInput(attrs={'v-model': 'email', ':disabled': 'fieldsDisable'}),
            'skype': forms.TextInput(attrs={'v-model': 'skype', ':disabled': 'fieldsDisable'}),
        }
