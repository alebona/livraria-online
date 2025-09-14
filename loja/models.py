# loja/models.py
from django.db import models
from django.conf import settings
from gestao.models import Livro

class Carrinho(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('A', 'Aprovado'),
        ('P', 'Pendente'),
        ('C', 'Cancelado'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use o user model do projeto
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    forma_pagamento = models.CharField(max_length=50, blank=True, null=True)

    def get_status_display_text(self):
        return dict(self.STATUS_CHOICES).get(self.status, "Desconhecido")

    def __str__(self):
        return f"Pedido #{self.id} - {self.user}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    livro = models.ForeignKey(Livro, on_delete=models.SET_NULL, null=True)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.livro.titulo} x {self.quantidade}"
