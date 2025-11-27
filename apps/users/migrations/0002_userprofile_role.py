# Generated manually: add role to user profile
from django.db import migrations, models
from django.contrib.auth import get_user_model


def populate_roles(apps, schema_editor):
    User = get_user_model()
    UserProfile = apps.get_model('users', 'UserProfile')
    for user in User.objects.all():
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': 'usuario'})
        if not created and not profile.role:
            profile.role = 'usuario'
            profile.save(update_fields=['role'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(
                choices=[
                    ('admin', 'Administrador'),
                    ('usuario', 'Usuario'),
                    ('vendedor', 'Vendedor oficial de cuentas'),
                    ('supervisor', 'Supervisor'),
                ],
                default='usuario',
                max_length=20,
            ),
        ),
        migrations.RunPython(populate_roles, migrations.RunPython.noop),
    ]
