# Generated manually: ensure existing profiles have role set
from django.db import migrations
def populate_roles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('users', 'UserProfile')
    for user in User.objects.all():
        profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': 'usuario'})
        if not created and not profile.role:
            profile.role = 'usuario'
            profile.save(update_fields=['role'])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_role'),
    ]

    operations = [
        migrations.RunPython(populate_roles, migrations.RunPython.noop),
    ]
