"""Forms for auth app."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from apps.users.models import UserProfile
import re

class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado de registro."""
    full_name = forms.CharField(max_length=100, required=False, label='Nombre y apellido')
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False, label='Teléfono')
    birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'phone', 'birthdate')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r"^[0-9+\-\s]{7,}$", phone):
            raise ValidationError("Teléfono inválido. Usa dígitos, espacios, '+' o '-'.")
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('full_name', '').split()[0] if self.cleaned_data.get('full_name') else ''
        user.last_name = ' '.join(self.cleaned_data.get('full_name', '').split()[1:]) if self.cleaned_data.get('full_name') else ''
        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.birthdate = self.cleaned_data.get('birthdate')
            profile.save()
        return user

class LoginForm(forms.Form):
    """Formulario de login."""
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, label='Recuérdame')
