from django.db import migrations
from django.conf import settings


def set_owner(apps, schema_editor):
    ClientEvent = apps.get_model('clients', 'ClientEvent')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    # Try to find the Arkangel user first, otherwise pick the first superuser, otherwise skip.
    owner = None
    try:
        owner = User.objects.filter(username='Arkangel').first()
    except Exception:
        owner = None
    if not owner:
        owner = User.objects.filter(is_superuser=True).order_by('id').first()
    if not owner:
        return
    ClientEvent.objects.filter(owner__isnull=True).update(owner=owner)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_clientevent_owner'),
    ]

    operations = [
        migrations.RunPython(set_owner, noop),
    ]
