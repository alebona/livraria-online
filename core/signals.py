from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

""" Atribuição automática de perfil ao criar usuário """
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
