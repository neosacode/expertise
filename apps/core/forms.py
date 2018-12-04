from django import forms
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
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        custom_attrs = {
            'username': {'class': 'form-control'},
            'email': {'class': 'form-control'},
            'first_name': {'class': 'form-control'},
            'last_name': {'class': 'form-control'},
            'password': {'class': 'form-control'},
        }
        required_fields = [
            'email',
            'first_name',
            'last_name',
        ]
