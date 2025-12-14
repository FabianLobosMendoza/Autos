"""Forms for clients app."""
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from .models import Client, CoHolder, ClientEvent, validate_cuit


class ClientForm(forms.ModelForm):
    """Formulario para Cliente con validaciones adicionales."""

    full_name = forms.CharField(
        label='Nombre y apellido o razón social',
        required=False,
        max_length=200,
    )

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            names = " ".join(part for part in [instance.first_name, instance.last_name] if part).strip()
            company = getattr(instance, 'company_name', '') or ''
            initial_name = names or company
            if initial_name:
                self.fields['full_name'].initial = initial_name

        if self.request_user:
            profile = getattr(self.request_user, 'profile', None)
            role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
            is_admin = self.request_user.is_superuser or role in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)
            if is_admin:
                qs = User.objects.filter(profile__role__in=[
                    UserProfile.ROLE_VENDOR,
                    UserProfile.ROLE_NEGOTIATOR,
                    UserProfile.ROLE_MANAGER,
                    UserProfile.ROLE_ACCOUNTANT,
                    UserProfile.ROLE_MARKETING,
                    UserProfile.ROLE_SUPERVISOR,
                    UserProfile.ROLE_ADMIN,
                ]).distinct()
                self.fields['owner'] = forms.ModelChoiceField(
                    queryset=qs,
                    required=False,
                    label='Asignar a',
                    widget=forms.Select(attrs={'class': 'form-select'})
                )
            else:
                if 'owner' in self.fields:
                    self.fields.pop('owner')

    class Meta:
        model = Client
        fields = [
            'owner',
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
            'employment',
            'email',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Paraguaya'}),
            'tax_condition': forms.Select(attrs={'class': 'form-select'}),
            'employment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Empleado, Independiente'}),
        }

    def clean(self):
        """Ensure either person name or company name is provided."""
        cleaned = super().clean()
        full_name = cleaned.get('full_name', '').strip()
        if not full_name:
            raise forms.ValidationError('Ingresar Nombre y apellido o Razón Social.')
        # Divide el nombre en nombre y apellido (o deja apellido vacío si no hay segundo término)
        parts = full_name.split(None, 1)
        cleaned['first_name'] = parts[0]
        cleaned['last_name'] = parts[1] if len(parts) > 1 else ''
        cleaned['company_name'] = full_name
        return cleaned

    def clean_cuit(self):
        value = self.cleaned_data.get('cuit', '')
        validate_cuit(value)
        return value


class ClientEventForm(forms.ModelForm):
    """Formulario para agendar eventos con clientes."""

    start_date = forms.DateField(
        label='Fecha',
        input_formats=['%d/%m/%Y'],
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'dd/mm/aaaa',
            'pattern': r'\d{2}/\d{2}/\d{4}',
            'inputmode': 'numeric',
            'maxlength': '10',
        }),
    )
    start_time = forms.TimeField(
        label='Hora',
        input_formats=['%H:%M'],
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'hh:mm (24h)',
            'pattern': r'\d{2}:\d{2}',
            'inputmode': 'numeric',
            'maxlength': '5',
        })
    )

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.request_user:
            profile = getattr(self.request_user, 'profile', None)
            role = getattr(profile, 'role', UserProfile.ROLE_VENDOR) if profile else UserProfile.ROLE_VENDOR
            is_admin = self.request_user.is_superuser or role in (UserProfile.ROLE_ADMIN, UserProfile.ROLE_SUPERVISOR)
            if not is_admin:
                self.fields['client'].queryset = Client.objects.filter(owner=self.request_user)
            if is_admin:
                qs_users = User.objects.filter(profile__role__in=[
                    UserProfile.ROLE_VENDOR,
                    UserProfile.ROLE_NEGOTIATOR,
                    UserProfile.ROLE_MANAGER,
                    UserProfile.ROLE_ACCOUNTANT,
                    UserProfile.ROLE_MARKETING,
                    UserProfile.ROLE_SUPERVISOR,
                    UserProfile.ROLE_ADMIN,
                ]).distinct()
                self.fields['owner'] = forms.ModelChoiceField(
                    queryset=qs_users,
                    required=False,
                    label='Asignar a',
                    widget=forms.Select(attrs={'class': 'form-select'})
                )
            else:
                if 'owner' in self.fields:
                    self.fields.pop('owner')
        # Campo starts_at queda oculto y se rellena combinando fecha + hora.
        self.fields['starts_at'].widget = forms.HiddenInput()
        self.fields['starts_at'].required = False

        # Si hay instancia, precarga fecha y hora.
        starts_at = getattr(self.instance, 'starts_at', None)
        if starts_at:
            self.fields['start_date'].initial = starts_at.date()
            self.fields['start_time'].initial = starts_at.time().replace(second=0, microsecond=0)

    class Meta:
        model = ClientEvent
        fields = ['title', 'client', 'starts_at', 'description', 'start_date', 'start_time', 'owner']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reunión de seguimiento'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas, lugar, agenda'}),
        }

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get('start_date')
        time = cleaned.get('start_time')
        if date and time:
            combined = datetime.datetime.combine(date, time)
            if timezone.is_naive(combined):
                combined = timezone.make_aware(combined, timezone.get_current_timezone())
            cleaned['starts_at'] = combined
        else:
            raise ValidationError('Completa fecha y hora.')
        return cleaned

    def save(self, commit=True):
        self.instance.starts_at = self.cleaned_data.get('starts_at')
        if 'owner' in self.cleaned_data and self.cleaned_data.get('owner'):
            self.instance.owner = self.cleaned_data.get('owner')
        elif self.request_user:
            self.instance.owner = self.request_user
        return super().save(commit=commit)


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
            'doc_type',
            'sex',
            'dni',
            'birth_date',
            'nationality',
            'phone',
            'employment',
            'email',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-select'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Paraguaya'}),
            'employment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Empleado, Independiente'}),
        }

    def clean(self):
        data = super().clean()
        provided = any(data.get(name) for name in self.fields.keys())
        if provided:
            missing = [name for name, value in data.items() if not value]
            if missing:
                raise ValidationError('Completa todos los campos del cotitular o deja todos vacios.')
        return data
