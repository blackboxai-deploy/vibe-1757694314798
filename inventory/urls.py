"""
URLs for inventory app
"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Entrada de produtos
    path('entrada/', views.entrada_list, name='entrada'),
    path('entrada/processar/<int:nota_id>/', views.processar_entrada, name='processar_entrada'),
    
    # Movimentação
    path('movimentacao/', views.movimentacao_list, name='movimentacao'),
    path('movimentacao/nova/', views.nova_movimentacao, name='nova_movimentacao'),
    path('movimentacao/<int:movimentacao_id>/', views.movimentacao_detail, name='movimentacao_detail'),
    
    # Análise
    path('analise/', views.analise_list, name='analise'),
    path('analise/nova/<int:estoque_id>/', views.nova_analise, name='nova_analise'),
    path('analise/<int:analise_id>/', views.analise_detail, name='analise_detail'),
    path('analise/<int:analise_id>/finalizar/', views.finalizar_analise, name='finalizar_analise'),
    
    # Fornecedores
    path('fornecedores/', views.fornecedor_list, name='fornecedores'),
    path('fornecedores/novo/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedores/<int:fornecedor_id>/', views.fornecedor_detail, name='fornecedor_detail'),
    path('fornecedores/<int:fornecedor_id>/editar/', views.fornecedor_edit, name='fornecedor_edit'),
    
    # Produtos
    path('produtos/', views.produto_list, name='produtos'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:produto_id>/', views.produto_detail, name='produto_detail'),
    path('produtos/<int:produto_id>/editar/', views.produto_edit, name='produto_edit'),
    
    # Estoque
    path('estoque/', views.estoque_list, name='estoque'),
    path('estoque/<int:estoque_id>/', views.estoque_detail, name='estoque_detail'),
    
    # Ajax endpoints
    path('ajax/produto-info/<int:produto_id>/', views.ajax_produto_info, name='ajax_produto_info'),
    path('ajax/estoque-disponivel/<int:produto_id>/', views.ajax_estoque_disponivel, name='ajax_estoque_disponivel'),
]