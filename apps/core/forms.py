from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.core.models import User


class ModelFormCustom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attributes = getattr(self.Meta, 'custom_attrs', {})

        for k, v in attributes.items():
            self.fields[k].widget.attrs.update(v)

        fields = getattr(self.Meta, 'required_fields', {})

        for name in fields:
            self.fields[name].required = True


class UserForm(ModelFormCustom):
    first_name = forms.CharField(max_length=100, label='Nome completo')

    class Meta:
        model = User
        fields = ['type', 'first_name', 'email', 'password', 'whatsapp', 'document', 'zipcode', 'address', 'number', 'district']
        widgets = {
            'password': forms.PasswordInput()
        }
        custom_attrs = {
            'type': {'class': 'form-control'},
            'email': {'class': 'form-control'},
            'first_name': {'class': 'form-control'},
            'whatsapp': {'class': 'form-control'},
            'document': {'class': 'form-control'},
            'password': {'class': 'form-control'},
            'zipcode': {'class': 'form-control'},
            'number': {'class': 'form-control'},
            'address': {'class': 'form-control'},
            'district': {'class': 'form-control'},
        }
        required_fields = [
            'email',
            'first_name',
            'password',
        ]

    def clean(self):
        cleaned_data = super().clean()
        signup_type = cleaned_data.get('type')
        whatsapp = cleaned_data.get('whatsapp')

        if signup_type != User.TYPE_CHOICES[1][0]:
            return

        if not whatsapp:
            self.add_error('whatsapp', _('This field is required'))

        if not document:
            self.add_error('document', _('This field is required'))