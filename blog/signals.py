from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a profile automatically when a new user is created.

    **Args:**

    - sender: The model that sent the signal (User).
    - instance: The user instance being created.
    - created: A boolean indicating if the user was created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the user's profile whenever the user instance is saved.

    **Args:**

    - sender: The model that sent the signal (User).
    - instance: The user instance being saved.
    """
    instance.profile.save()
