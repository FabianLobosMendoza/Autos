"""Signals for users app."""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import UserProfile


@receiver(post_save, sender=User)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    """Ensure profile exists for every new user."""
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': UserProfile.ROLE_VENDOR},
        )
