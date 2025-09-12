#!/usr/bin/env python3
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from inventory.models import (
    Departamento, CategoriaProduto, Produto, Fornecedor
)
from accounts.models import UserPermission

User = get_user_model()

# Create departments
departments = [
    {'nome': 'Departamento de Análise', 'tipo': 'analise'},
    {'nome': 'Departamento Laboratorial', 'tipo': 'laboratorio'},
    {'nome': 'Departamento Industrial', 'tipo': 'industrial'},
    {'nome': 'Estoque Central', 'tipo': 'estoque'},
    {'nome': 'Expedição', 'tipo': 'expedicao'},
]

for dept_data in departments:
    dept, created = Departamento.objects.get_or_create(
        nome=dept_data['nome'],
        defaults={'tipo': dept_data['tipo'], 'ativo': True}
    )
    if created:
        print(f"✓ Departamento criado: {dept.nome}")
    else:
        print(f"- Departamento já existe: {dept.nome}")

# Create product categories
categories = [
    {'nome': 'Matéria Prima', 'descricao': 'Ingredientes básicos para produção'},
    {'nome': 'Químicos', 'descricao': 'Produtos químicos diversos'},
    {'nome': 'Equipamentos', 'descricao': 'Equipamentos e ferramentas'},
    {'nome': 'Embalagens', 'descricao': 'Materiais de embalagem'},
    {'nome': 'Consumíveis', 'descricao': 'Itens de consumo geral'},
]

for cat_data in categories:
    category, created = CategoriaProduto.objects.get_or_create(
        nome=cat_data['nome'],
        defaults={'descricao': cat_data['descricao'], 'ativo': True}
    )
    if created:
        print(f"✓ Categoria criada: {category.nome}")
    else:
        print(f"- Categoria já existe: {category.nome}")

# Create suppliers
suppliers = [
    {
        'nome_empresa': 'Fornecedor Alpha Ltda',
        'cnpj': '12345678901234',
        'email_contato': 'contato@alpha.com',
        'telefone': '(11) 1234-5678',
        'endereco_completo': 'Rua das Indústrias, 123 - São Paulo/SP',
        'pessoa_contato': 'João Silva'
    },
    {
        'nome_empresa': 'Beta Química S.A.',
        'cnpj': '56789012345678',
        'email_contato': 'vendas@betaquimica.com',
        'telefone': '(11) 9876-5432',
        'endereco_completo': 'Av. Química, 456 - São Paulo/SP',
        'pessoa_contato': 'Maria Santos'
    },
    {
        'nome_empresa': 'Gamma Equipamentos',
        'cnpj': '98765432109876',
        'email_contato': 'info@gamma.com.br',
        'telefone': '(11) 5555-1234',
        'endereco_completo': 'Rod. Industrial, 789 - Guarulhos/SP',
        'pessoa_contato': 'Pedro Oliveira'
    }
]

for supplier_data in suppliers:
    supplier, created = Fornecedor.objects.get_or_create(
        cnpj=supplier_data['cnpj'],
        defaults=supplier_data
    )
    if created:
        print(f"✓ Fornecedor criado: {supplier.nome_empresa}")
    else:
        print(f"- Fornecedor já existe: {supplier.nome_empresa}")

# Create sample products
products = [
    {
        'codigo_produto': 'MP001',
        'nome_produto': 'Ácido Sulfúrico 98%',
        'categoria': 'Químicos',
        'descricao': 'Ácido sulfúrico concentrado para processos industriais',
        'unidade_medida': 'L',
        'preco_unitario': 15.50,
        'estoque_minimo': 50,
        'requer_analise': True,
        'tempo_analise_dias': 3
    },
    {
        'codigo_produto': 'MP002',
        'nome_produto': 'Soda Cáustica',
        'categoria': 'Químicos',
        'descricao': 'Hidróxido de sódio em escamas',
        'unidade_medida': 'KG',
        'preco_unitario': 8.75,
        'estoque_minimo': 100,
        'requer_analise': True,
        'tempo_analise_dias': 2
    },
    {
        'codigo_produto': 'EQ001',
        'nome_produto': 'Bomba Centrífuga 5HP',
        'categoria': 'Equipamentos',
        'descricao': 'Bomba centrífuga para processos industriais',
        'unidade_medida': 'UN',
        'preco_unitario': 2500.00,
        'estoque_minimo': 2,
        'requer_analise': False,
        'tempo_analise_dias': 0
    },
    {
        'codigo_produto': 'EMB001',
        'nome_produto': 'Tambor Plástico 200L',
        'categoria': 'Embalagens',
        'descricao': 'Tambor plástico para armazenamento',
        'unidade_medida': 'UN',
        'preco_unitario': 85.00,
        'estoque_minimo': 10,
        'requer_analise': False,
        'tempo_analise_dias': 0
    },
    {
        'codigo_produto': 'CON001',
        'nome_produto': 'EPI - Luvas Nitrílicas',
        'categoria': 'Consumíveis',
        'descricao': 'Luvas de proteção em nitrilo',
        'unidade_medida': 'CX',
        'preco_unitario': 45.00,
        'estoque_minimo': 25,
        'requer_analise': False,
        'tempo_analise_dias': 0
    }
]

for prod_data in products:
    categoria = CategoriaProduto.objects.get(nome=prod_data['categoria'])
    prod_data['categoria'] = categoria
    
    produto, created = Produto.objects.get_or_create(
        codigo_produto=prod_data['codigo_produto'],
        defaults=prod_data
    )
    if created:
        print(f"✓ Produto criado: {produto.codigo_produto} - {produto.nome_produto}")
    else:
        print(f"- Produto já existe: {produto.codigo_produto}")

# Create a test user with limited permissions
test_user_data = {
    'email': 'teste@exemplo.com',
    'username': 'teste@exemplo.com',
    'first_name': 'Usuário',
    'last_name': 'Teste',
    'is_email_verified': True
}

test_user, created = User.objects.get_or_create(
    email='teste@exemplo.com',
    defaults=test_user_data
)

if created:
    test_user.set_password('teste123')
    test_user.save()
    print(f"✓ Usuário de teste criado: {test_user.email} (senha: teste123)")
else:
    print(f"- Usuário de teste já existe: {test_user.email}")

# Grant some permissions to test user
permissions_to_grant = [
    ('dashboard', 'view'),
    ('produtos', 'view'),
    ('fornecedores', 'view'),
    ('entrada', 'view'),
    ('movimentacao', 'view'),
]

admin_user = User.objects.get(username='admin')

for module, permission in permissions_to_grant:
    user_perm, created = UserPermission.objects.get_or_create(
        user=test_user,
        module=module,
        permission=permission,
        defaults={'granted_by': admin_user, 'is_active': True}
    )
    if created:
        print(f"✓ Permissão concedida: {test_user.email} - {module} ({permission})")
    else:
        print(f"- Permissão já existe: {test_user.email} - {module} ({permission})")

print("\n🎉 Dados de exemplo criados com sucesso!")
print("\n📋 Credenciais de acesso:")
print("👤 Admin: admin / admin123 (acesso completo)")
print("👤 Teste: teste@exemplo.com / teste123 (acesso limitado)")
print(f"🌐 URL: https://sb-1ozvh6m5c6l8.vercel.run")