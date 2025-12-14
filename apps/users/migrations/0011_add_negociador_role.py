from django.db import migrations


def convert_existing_vendors_to_negociador(apps, schema_editor):
    UserProfile = apps.get_model('users', 'UserProfile')
    UserProfile.objects.filter(role='vendedor').update(role='negociador')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_convert_usuario_to_vendedor'),
    ]

    operations = [
        migrations.RunPython(convert_existing_vendors_to_negociador, noop),
    ]
