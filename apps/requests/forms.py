from django import forms

from apps.requests.models import UrlPriority


class UrlPriorityForm(forms.ModelForm):
    class Meta:
        model = UrlPriority
        fields = ('priority',)

    def clean_priority(self):
        if not self.cleaned_data.get('priority'):
            return 1
        else:
            return self.cleaned_data.get('priority')
