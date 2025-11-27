"""Forms for clients app."""
from django import forms
from django.core.exceptions import ValidationError
from .models import Client, CoHolder, validate_cuit


class ClientForm(forms.ModelForm):
    """Formulario para Cliente con validaciones adicionales."""

    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'doc_type',
            'doc_number',
            'birth_date',
            'sex',
            'marital_status',
            'nationality',
            'tax_condition',
            'cuit',
            'street',
            'street_number',
            'floor',
            'apartment',
            'postal_code',
            'city',
            'province',
            'phone',
            'email',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.Select(attrs={'class': 'form-select'}),
            'tax_condition': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        """Ensure either person name or company name is provided."""
        cleaned = super().clean()
        first_name = cleaned.get('first_name', '').strip()
        last_name = cleaned.get('last_name', '').strip()
        company = cleaned.get('company_name', '').strip()
        if not ((first_name and last_name) or company):
            raise forms.ValidationError('Ingresar Apellido y Nombre o Razón Social.')
        return cleaned

    def clean_cuit(self):
        value = self.cleaned_data.get('cuit', '')
        validate_cuit(value)
        return value


class CoHolderForm(forms.ModelForm):
    """Formulario para Cotitular (opcional)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    class Meta:
        model = CoHolder
        fields = [
            'full_name',
            'sex',
            'dni',
            'birth_date',
            'nationality',
            'phone',
            'email',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        data = super().clean()
        provided = any(data.get(name) for name in self.fields.keys())
        if provided:
            missing = [name for name, value in data.items() if not value]
            if missing:
                raise ValidationError('Completa todos los campos del cotitular o deja todos vacios.')
        return data
