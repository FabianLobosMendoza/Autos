# Generated manually: align existing profiles with is_staff flag
from django.db import migrations


def sync_roles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('users', 'UserProfile')
    for user in User.objects.all():
        profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'role': 'usuario'})
        desired_role = 'admin' if user.is_staff or user.is_superuser else profile.role or 'usuario'
        if profile.role != desired_role:
            profile.role = desired_role
            profile.save(update_fields=['role'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_populate_roles'),
    ]

    operations = [
        migrations.RunPython(sync_roles, migrations.RunPython.noop),
    ]
