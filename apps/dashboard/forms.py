from django import forms
from apps.core.models import Analyze


class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyze
        fields = ['zipcode', 'address', 'number', 'registration_number', 'block', 'lot', 'type', 'complement']
        widgets = {
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código postal'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Não coloque cidade e estado'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coloque 0 se não existir'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'block': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'lot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'complement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira informações complementares do imóvel'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
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
