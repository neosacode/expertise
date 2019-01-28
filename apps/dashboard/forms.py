from django import forms
from apps.core.models import Analyze


class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyze
        fields = ['zipcode', 'address', 'number', 'registration_number', 'block', 'lot']
        widgets = {
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000-000'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua de exemplo'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000000'}),
            'block': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000'}),
            'lot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lot'].required = False
        self.fields['registration_number'].required = False
        self.fields['block'].required = False

    def clean(self):
        cleaned_data = super().clean()
        registration_number = cleaned_data.get('registration_number')
        block = cleaned_data.get('block')
        lot = cleaned_data.get('lot')

        if not registration_number and not block and not lot:
            self.add_error('registration_number', 'Preencha a matrícula, ou quadra e lote')

        if not registration_number and block and not lot:
            self.add_error('lot', 'Este campo é obrigatório')
