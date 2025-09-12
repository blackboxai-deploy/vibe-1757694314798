"""
Core models for Stock Management System
"""
from django.db import models


class Cliente(models.Model):
    """
    Modelo de Cliente - representa uma empresa que usa o sistema
    """
    nome_empresa = models.CharField(
        max_length=100,
        verbose_name="Nome da Empresa"
    )
    
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        help_text="CNPJ da empresa (formato: XX.XXX.XXX/XXXX-XX)"
    )
    
    email_contato = models.EmailField(
        verbose_name="Email de Contato"
    )
    
    telefone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone"
    )
    
    endereco = models.TextField(
        blank=True,
        verbose_name="Endereço Completo"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    # Configurações específicas do cliente
    configuracoes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Configurações",
        help_text="Configurações específicas do cliente em formato JSON"
    )
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome_empresa']
    
    def __str__(self):
        return f"{self.nome_empresa} ({self.cnpj})"
    
    @property
    def is_active(self):
        return self.ativo