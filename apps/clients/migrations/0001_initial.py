# Generated manually for clients app
from django.db import migrations, models
import django.db.models.deletion
import apps.clients.models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=100, verbose_name='Apellido')),
                ('company_name', models.CharField(blank=True, max_length=150, verbose_name='Razón Social')),
                ('doc_type', models.CharField(choices=[('LE', 'Libreta de Enrolamiento (LE)'), ('LC', 'Libreta Cívica (LC)'), ('DNI', 'DNI')], max_length=3, verbose_name='Tipo de Documento')),
                ('doc_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d+$', 'Solo se permiten números.')], verbose_name='Número de Documento')),
                ('birth_date', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Sexo')),
                ('marital_status', models.CharField(choices=[('casado', 'Casado'), ('soltero', 'Soltero'), ('divorciado', 'Divorciado')], max_length=10, verbose_name='Estado Civil')),
                ('nationality', models.CharField(choices=[('argentino', 'Argentino'), ('naturalizado', 'Naturalizado'), ('extranjero', 'Extranjero')], max_length=20, verbose_name='Nacionalidad')),
                ('tax_condition', models.CharField(choices=[('cf', 'Consumidor Final (CF)'), ('ri', 'Responsable Inscripto'), ('rm', 'Responsable Monotributo'), ('exento', 'Exento')], max_length=10, verbose_name='Condición Fiscal')),
                ('cuit', models.CharField(max_length=11, validators=[apps.clients.models.validate_cuit], verbose_name='CUIT/CUIL')),
                ('street', models.CharField(max_length=150, verbose_name='Calle')),
                ('street_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d+$', 'Solo números.')], verbose_name='Número')),
                ('floor', models.CharField(blank=True, max_length=10, verbose_name='Piso')),
                ('apartment', models.CharField(blank=True, max_length=10, verbose_name='Depto')),
                ('postal_code', models.CharField(max_length=10, verbose_name='Código Postal')),
                ('city', models.CharField(max_length=100, verbose_name='Localidad')),
                ('province', models.CharField(max_length=100, verbose_name='Provincia')),
                ('phone', models.CharField(max_length=30, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['last_name', 'company_name'],
            },
        ),
        migrations.CreateModel(
            name='CoHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Apellido y Nombre')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Sexo')),
                ('dni', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d+$', 'Solo números.')], verbose_name='DNI')),
                ('birth_date', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('nationality', models.CharField(choices=[('argentino', 'Argentino'), ('naturalizado', 'Naturalizado'), ('extranjero', 'Extranjero')], max_length=20, verbose_name='Nacionalidad')),
                ('phone', models.CharField(max_length=30, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coholder', to='clients.client')),
            ],
            options={
                'verbose_name': 'Cotitular',
                'verbose_name_plural': 'Cotitulares',
            },
        ),
        migrations.AddIndex(
            model_name='client',
            index=models.Index(fields=['last_name'], name='clients_cli_last_na_472c33_idx'),
        ),
        migrations.AddIndex(
            model_name='client',
            index=models.Index(fields=['company_name'], name='clients_cli_company_713ae6_idx'),
        ),
        migrations.AddIndex(
            model_name='client',
            index=models.Index(fields=['cuit'], name='clients_cli_cuit_d6a3e5_idx'),
        ),
    ]
