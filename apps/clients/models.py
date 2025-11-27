"""Models for clients app."""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.db import models


DOC_TYPE_CHOICES = [
    ('LE', 'Libreta de Enrolamiento (LE)'),
    ('LC', 'Libreta Cívica (LC)'),
    ('DNI', 'DNI'),
]

SEX_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]

MARITAL_STATUS_CHOICES = [
    ('casado', 'Casado'),
    ('soltero', 'Soltero'),
    ('divorciado', 'Divorciado'),
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
    nationality = models.CharField('Nacionalidad', max_length=20, choices=NATIONALITY_CHOICES)

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
    sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES)
    dni = models.CharField('DNI', max_length=15, validators=[RegexValidator(r'^\d+$', 'Solo números.')])
    birth_date = models.DateField('Fecha de Nacimiento')
    nationality = models.CharField('Nacionalidad', max_length=20, choices=NATIONALITY_CHOICES)
    phone = models.CharField('Teléfono', max_length=30)
    email = models.EmailField('Correo Electrónico', validators=[EmailValidator()])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cotitular de {self.client}"

    class Meta:
        verbose_name = 'Cotitular'
        verbose_name_plural = 'Cotitulares'
