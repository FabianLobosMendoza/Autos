from django.db import migrations


def convert_usuario(apps, schema_editor):
    UserProfile = apps.get_model('users', 'UserProfile')
    UserProfile.objects.filter(role='usuario').update(role='vendedor')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_sync_role_with_staff'),
    ]

    operations = [
        migrations.RunPython(convert_usuario, noop),
    ]
