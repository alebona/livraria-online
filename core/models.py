from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nome_completo = models.CharField(max_length=150, blank=False)
    endereco = models.CharField(max_length=255, blank=False)
    numero_endereco = models.CharField(max_length=20, blank=False, null=True)    
    bairro = models.CharField(max_length=100, blank=False, null=True)
    cidade = models.CharField(max_length=100, blank=False, null=True)
    estado = models.CharField(max_length=100, blank=False, null=True)
    cep = models.CharField(max_length=20, blank=False, null=True)
    email = models.EmailField(unique=True, blank=False)

    REQUIRED_FIELDS = ["nome_completo", "endereco", "numero_endereco", "bairro", "cidade", "estado", "cep", "email"]

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    PERFIL_CHOICES = (
        ('Administrador', 'Administrador'),
        ('Cliente', 'Cliente'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='Cliente')

    def __str__(self):
        return f"{self.user.username} - {self.perfil}"
