"""
Admin configuration for Core app
"""
from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Admin para gerenciamento de Clientes
    """
    list_display = [
        'nome_empresa', 
        'cnpj', 
        'email_contato', 
        'ativo', 
        'data_criacao'
    ]
    
    list_filter = [
        'ativo', 
        'data_criacao',
        'data_atualizacao'
    ]
    
    search_fields = [
        'nome_empresa', 
        'cnpj', 
        'email_contato'
    ]
    
    readonly_fields = [
        'data_criacao', 
        'data_atualizacao'
    ]
    
    fieldsets = (
        ('Informações da Empresa', {
            'fields': (
                'nome_empresa',
                'cnpj',
                'email_contato',
                'telefone',
                'endereco'
            )
        }),
        ('Configurações do Sistema', {
            'fields': (
                'ativo',
                'configuracoes'
            )
        }),
        ('Informações de Auditoria', {
            'fields': (
                'data_criacao',
                'data_atualizacao'
            ),
            'classes': ('collapse',)
        })
    )