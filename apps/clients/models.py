"""Models for clients app."""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

DOC_TYPE_CHOICES = [
    ('LE', 'Libreta de Enrolamiento (LE)'),
    ('LC', 'Libreta Cívica (LC)'),
    ('DNI', 'DNI'),
    ('PAS', 'Pasaporte'),
]

SEX_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otros'),
]

MARITAL_STATUS_CHOICES = [
    ('casado', 'Casado'),
    ('soltero', 'Soltero'),
    ('divorciado', 'Divorciado'),
    ('viudo', 'Viudo'),
]

NATIONALITY_CHOICES = [
    ('argentino', 'Argentino'),
    ('naturalizado', 'Naturalizado'),
    ('extranjero', 'Extranjero'),
]

TAX_CONDITION_CHOICES = [
    ('cf', 'Consumidor Final (CF)'),
    ('ri', 'Responsable Inscripto'),
    ('rm', 'Responsable Monotributo'),
    ('exento', 'Exento'),
]


def validate_cuit(value: str):
    """Validate CUIT/CUIL check digit."""
    digits = ''.join(filter(str.isdigit, value or ''))
    if len(digits) != 11:
        raise ValidationError('El CUIT/CUIL debe tener 11 dígitos.')

    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(digits[:10], weights))
    mod = total % 11
    check_digit = 11 - mod
    if check_digit == 11:
        check_digit = 0
    elif check_digit == 10:
        check_digit = 9
    if check_digit != int(digits[-1]):
        raise ValidationError('CUIT/CUIL inválido (dígito verificador).')


class Client(models.Model):
    """Datos del cliente titular."""
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clients_owned')
    # Identidad
    first_name = models.CharField('Nombre', max_length=100, blank=True)
    last_name = models.CharField('Apellido', max_length=100, blank=True)
    company_name = models.CharField('Razón Social', max_length=150, blank=True)
    doc_type = models.CharField('Tipo de Documento', max_length=3, choices=DOC_TYPE_CHOICES)
    doc_number = models.CharField(
        'Número de Documento',
        max_length=15,
        validators=[RegexValidator(r'^\d+$', 'Solo se permiten números.')],
    )
    birth_date = models.DateField('Fecha de Nacimiento')
    sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES)
    marital_status = models.CharField('Estado Civil', max_length=10, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField('Nacionalidad', max_length=50)

    # Datos fiscales
    tax_condition = models.CharField('Condición Fiscal', max_length=10, choices=TAX_CONDITION_CHOICES)
    cuit = models.CharField('CUIT/CUIL', max_length=11, validators=[validate_cuit])

    # Domicilio
    street = models.CharField('Calle', max_length=150)
    street_number = models.CharField('Número', max_length=10, validators=[RegexValidator(r'^\d+$', 'Solo números.')])
    floor = models.CharField('Piso', max_length=10, blank=True)
    apartment = models.CharField('Depto', max_length=10, blank=True)
    postal_code = models.CharField('Código Postal', max_length=10)
    city = models.CharField('Localidad', max_length=100)
    province = models.CharField('Provincia', max_length=100)

    # Contacto
    phone = models.CharField('Teléfono', max_length=30)
    email = models.EmailField('Correo Electrónico', validators=[EmailValidator()])
    employment = models.CharField('Empleo / Ocupación', max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display_name = self.company_name if self.company_name else f"{self.last_name}, {self.first_name}".strip(', ')
        return display_name or f"Cliente {self.id}"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['last_name', 'company_name']
        indexes = [
            models.Index(fields=['last_name']),
            models.Index(fields=['company_name']),
            models.Index(fields=['cuit']),
        ]


class CoHolder(models.Model):
    """Datos de cónyuge o cotitular (opcional)."""
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='coholder')
    full_name = models.CharField('Apellido y Nombre', max_length=150)
    doc_type = models.CharField('Tipo de Documento', max_length=3, choices=DOC_TYPE_CHOICES, default='DNI')
    sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES)
    dni = models.CharField('DNI', max_length=15, validators=[RegexValidator(r'^\d+$', 'Solo números.')])
    birth_date = models.DateField('Fecha de Nacimiento')
    nationality = models.CharField('Nacionalidad', max_length=50)
    phone = models.CharField('Teléfono', max_length=30)
    email = models.EmailField('Correo Electrónico', validators=[EmailValidator()])
    employment = models.CharField('Empleo / Ocupación', max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cotitular de {self.client}"

    class Meta:
        verbose_name = 'Cotitular'
        verbose_name_plural = 'Cotitulares'


class ClientEvent(models.Model):
    """Evento agendado con un cliente (opcional si es solo lead)."""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    lead = models.ForeignKey('ClientLead', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_events', null=True, blank=True)
    title = models.CharField('Título', max_length=150)
    description = models.TextField('Notas', blank=True)
    starts_at = models.DateTimeField('Fecha y hora')
    lead_name = models.CharField('Nombre lead', max_length=150, blank=True)
    lead_phone = models.CharField('Teléfono lead', max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento de cliente'
        verbose_name_plural = 'Eventos de cliente'
        ordering = ['starts_at']
        indexes = [
            models.Index(fields=['starts_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.client} ({self.starts_at:%Y-%m-%d %H:%M})"


class ClientLead(models.Model):
    """Cliente rápido de publicidad (datos opcionales)."""
    name = models.CharField('Nombre', max_length=150, blank=True)
    phone = models.CharField('Teléfono', max_length=30, blank=True)
    source = models.CharField('Fuente (publicidad)', max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_leads')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente rápido'
        verbose_name_plural = 'Clientes rápidos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f"Lead {self.id}"


class ClientLeadNote(models.Model):
    """Notas históricas de un cliente rápido (append-only)."""
    lead = models.ForeignKey(ClientLead, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Nota de cliente rápido'
        verbose_name_plural = 'Notas de cliente rápido'

    def __str__(self):
        return f"Nota de {self.author or 'Sistema'} en lead {self.lead_id}"


class LeadInterview(models.Model):
    """Entrevista agendada para un lead (sin requerir cliente)."""
    lead = models.ForeignKey(ClientLead, on_delete=models.CASCADE, related_name='interviews')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_interviews')
    title = models.CharField('Título', max_length=150)
    scheduled_at = models.DateTimeField('Fecha y hora')
    notes = models.TextField('Notas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']
        verbose_name = 'Entrevista de lead'
        verbose_name_plural = 'Entrevistas de lead'

    def __str__(self):
        return f"{self.title} ({self.scheduled_at:%Y-%m-%d %H:%M})"


class ClientNote(models.Model):
    """Notas del cliente (solo se agregan, no se borran)."""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField('Nota')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nota de cliente'
        verbose_name_plural = 'Notas de cliente'
        ordering = ['-created_at']

    def __str__(self):
        author_name = self.author.username if self.author else 'Sistema'
        return f"Nota de {author_name} en {self.client} - {self.created_at:%Y-%m-%d}"
