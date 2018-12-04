from django import forms
from apps.core.models import Analyze


class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyze
        fields = []