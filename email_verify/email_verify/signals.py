from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailVerification
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_email_verification(sender, instance=None, created=False, **kwargs):
    # we do not want this logic to run when `createsuperuser` is used
    if created and not instance.is_superuser:
        EmailVerification.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_email_verification(sender, instance=None, **kwargs):
    if not instance.is_superuser:
        instance.emailverification.save()