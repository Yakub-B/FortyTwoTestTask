from django import forms

from apps.requests.models import RequestModel


class RequestPriorityForm(forms.ModelForm):
    class Meta:
        model = RequestModel
        fields = ('priority',)
