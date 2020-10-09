from django import forms

from apps.requests.models import UrlPriority


class UrlPriorityForm(forms.ModelForm):
    class Meta:
        model = UrlPriority
        fields = ('priority',)

    def clean_priority(self):
        # QueryDict.get('', 1) will return ''
        priority = self.cleaned_data.get('priority')
        if not priority:
            return 1
        return priority
