"""
User models for Stock Management System
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado com verificação de email
    """
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="Email Verificado"
    )
    
    email_verification_token = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Token de Verificação"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone"
    )
    
    department = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Departamento"
    )
    
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cargo"
    )
    
    theme_preference = models.CharField(
        max_length=10,
        choices=[
            ('light', 'Claro'),
            ('dark', 'Escuro'),
            ('auto', 'Automático')
        ],
        default='auto',
        verbose_name="Tema Preferido"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Auto-generate username from email if not provided
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


class UserPermission(models.Model):
    """
    Sistema de permissões granulares por usuário
    """
    PERMISSION_CHOICES = [
        ('view', 'Visualizar'),
        ('create', 'Criar'),
        ('edit', 'Editar'),
        ('delete', 'Excluir'),
        ('export', 'Exportar'),
    ]
    
    MODULE_CHOICES = [
        ('dashboard', 'Dashboard'),
        ('entrada', 'Entrada de Produtos'),
        ('movimentacao', 'Movimentação'),
        ('analise', 'Análise'),
        ('fornecedores', 'Fornecedores'),
        ('produtos', 'Produtos'),
        ('relatorios', 'Relatórios'),
        ('configuracoes', 'Configurações'),
        ('nota_fiscal', 'Nota Fiscal'),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='custom_permissions',
        verbose_name="Usuário"
    )
    
    module = models.CharField(
        max_length=50,
        choices=MODULE_CHOICES,
        verbose_name="Módulo"
    )
    
    permission = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES,
        verbose_name="Permissão"
    )
    
    granted_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permissions_granted',
        verbose_name="Concedido por"
    )
    
    granted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Concessão"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    class Meta:
        verbose_name = "Permissão de Usuário"
        verbose_name_plural = "Permissões de Usuário"
        unique_together = ['user', 'module', 'permission']
        ordering = ['user', 'module', 'permission']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_module_display()} - {self.get_permission_display()}"


class UserRole(models.Model):
    """
    Modelo para papéis/funções de usuário
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome da Função"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    users = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='roles',
        verbose_name="Usuários"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    class Meta:
        verbose_name = "Função de Usuário"
        verbose_name_plural = "Funções de Usuário"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserActivity(models.Model):
    """
    Log de atividades dos usuários
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name="Usuário"
    )
    
    action = models.CharField(
        max_length=100,
        verbose_name="Ação"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Endereço IP"
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data/Hora"
    )
    
    class Meta:
        verbose_name = "Atividade do Usuário"
        verbose_name_plural = "Atividades dos Usuários"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.action} - {self.timestamp}"