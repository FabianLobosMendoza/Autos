"""Forms for clients app."""
from django import forms
from django.core.exceptions import ValidationError
from .models import Client, CoHolder, validate_cuit


class ClientForm(forms.ModelForm):
    """Formulario para Cliente con validaciones adicionales."""

    full_name = forms.CharField(
        label='Nombre y apellido o razón social',
        required=False,
        max_length=200,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            names = " ".join(part for part in [instance.first_name, instance.last_name] if part).strip()
            company = getattr(instance, 'company_name', '') or ''
            initial_name = names or company
            if initial_name:
                self.fields['full_name'].initial = initial_name

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
        full_name = cleaned.get('full_name', '').strip()
        if not full_name:
            raise forms.ValidationError('Ingresar Nombre y apellido o Razón Social.')
        if full_name:
            cleaned['first_name'] = full_name
            cleaned['last_name'] = full_name
            cleaned['company_name'] = full_name
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
